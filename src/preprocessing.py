from pathlib import Path
from typing import Tuple
import cv2
import numpy as np
import pandas as pd
from PIL import Image

# ==========================================================
# RUTAS DEL PROYECTO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CROPS_DIR = BASE_DIR / "data" / "crops"
OUTPUT_DIR = BASE_DIR / "data" / "output"

TARGET_SIZE = (1000, 1600)  # ancho, alto

# Coordenadas relativas: (x1, y1, x2, y2)
CROP_AREAS = {
    "total_sufragantes": (0.048, 0.261, 0.304, 0.290),
    "votos_en_urna": (0.357, 0.261, 0.611, 0.290),
    "votos_incinerados": (0.672, 0.264, 0.927, 0.289),

    "votos_candidato_1": (0.674, 0.345, 0.936, 0.386),
    "votos_candidato_2": (0.670, 0.444, 0.930, 0.489),

    "votos_blanco": (0.669, 0.516, 0.925, 0.548),
    "votos_nulos": (0.670, 0.547, 0.925, 0.577),
    "votos_no_marcados": (0.675, 0.574, 0.922, 0.603),
    "total_mesa": (0.662, 0.600, 0.925, 0.633),
}


# ==========================================================
# CARPETAS Y ARCHIVOS
# ==========================================================

def ensure_dirs() -> None:
    for folder in [RAW_DIR, PROCESSED_DIR, CROPS_DIR, OUTPUT_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def list_input_files(raw_dir: Path = RAW_DIR) -> list[Path]:
    """
    Busca PDFs e imágenes dentro de data/raw/, incluyendo subcarpetas.
    """
    valid_ext = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}
    raw_dir.mkdir(parents=True, exist_ok=True)

    return sorted([
        p for p in raw_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in valid_ext
    ])


def get_form_id(path: Path) -> str:
    """
    Devuelve el ID del formulario.

    Ejemplo:
    data/raw/E14Cali_Zona13_01/E14_001.pdf
    -> E14_001

    Así las salidas quedan organizadas por formulario.
    """
    return path.stem


# ==========================================================
# CARGA PDF / IMAGEN
# ==========================================================

def pdf_first_page_to_image(pdf_path: Path, dpi: int = 220) -> Image.Image:
    """
    Convierte la primera página de un PDF a imagen.
    Requiere instalar PyMuPDF:
    pip install pymupdf
    """
    import fitz

    doc = fitz.open(str(pdf_path))
    page = doc[0]

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    pix = page.get_pixmap(matrix=matrix, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    doc.close()
    return img


def load_document_as_image(path: Path) -> Image.Image:
    """
    Carga un PDF o una imagen.
    """
    if path.suffix.lower() == ".pdf":
        return pdf_first_page_to_image(path)

    return Image.open(path).convert("RGB")


# ==========================================================
# PREPROCESAMIENTO
# ==========================================================

def preprocess_image(
    pil_img: Image.Image,
    target_size: Tuple[int, int] = TARGET_SIZE
) -> np.ndarray:
    """
    Preprocesa el formulario:
    - escala de grises
    - redimensionamiento
    - mejora de contraste
    - reducción de ruido
    - binarización
    """
    img = np.array(pil_img.convert("RGB"))

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    denoised = cv2.medianBlur(enhanced, 3)

    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        35,
        11
    )

    return binary


def save_processed_image(processed: np.ndarray, form_id: str) -> Path:
    """
    Guarda la imagen procesada dentro de:
    data/processed/E14_001/E14_001_processed.png
    """
    form_processed_dir = PROCESSED_DIR / form_id
    form_processed_dir.mkdir(parents=True, exist_ok=True)

    out_path = form_processed_dir / f"{form_id}_processed.png"
    cv2.imwrite(str(out_path), processed)

    return out_path


# ==========================================================
# RECORTES
# ==========================================================

def relative_to_absolute_coords(
    rel_coords: Tuple[float, float, float, float],
    width: int,
    height: int
) -> Tuple[int, int, int, int]:
    x1, y1, x2, y2 = rel_coords

    return (
        int(x1 * width),
        int(y1 * height),
        int(x2 * width),
        int(y2 * height)
    )


def crop_fields(
    processed_img: np.ndarray,
    form_id: str,
    crop_areas=CROP_AREAS
) -> list[dict]:
    """
    Genera recortes automáticos y los guarda en:
    data/crops/E14_001/nombre_campo.png
    """
    h, w = processed_img.shape[:2]

    form_crop_dir = CROPS_DIR / form_id
    form_crop_dir.mkdir(parents=True, exist_ok=True)

    records = []

    for field_name, rel_coords in crop_areas.items():
        x1, y1, x2, y2 = relative_to_absolute_coords(rel_coords, w, h)

        x1 = max(0, min(x1, w))
        x2 = max(0, min(x2, w))
        y1 = max(0, min(y1, h))
        y2 = max(0, min(y2, h))

        crop = processed_img[y1:y2, x1:x2]

        crop_path = form_crop_dir / f"{field_name}.png"
        cv2.imwrite(str(crop_path), crop)

        records.append({
            "form_id": form_id,
            "field": field_name,
            "crop_path": str(crop_path).replace("\\", "/"),
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        })

    return records


def draw_crop_preview(
    processed_img: np.ndarray,
    out_path: Path,
    crop_areas=CROP_AREAS
) -> Path:
    """
    Guarda una vista previa con rectángulos rojos en:
    data/output/E14_001/E14_001_preview_recortes.png
    """
    h, w = processed_img.shape[:2]

    preview = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)

    for field_name, rel_coords in crop_areas.items():
        x1, y1, x2, y2 = relative_to_absolute_coords(rel_coords, w, h)

        cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.putText(
            preview,
            field_name,
            (x1, max(25, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            1,
            cv2.LINE_AA
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), preview)

    return out_path


# ==========================================================
# PIPELINE PRINCIPAL
# ==========================================================

def process_one_file(path: Path, save_preview: bool = True) -> list[dict]:
    """
    Procesa un solo formulario.

    Entrada:
    data/raw/.../E14_001.pdf

    Salidas:
    data/processed/E14_001/
    data/crops/E14_001/
    data/output/E14_001/
    """
    ensure_dirs()

    form_id = get_form_id(path)

    original = load_document_as_image(path)
    processed = preprocess_image(original)

    processed_path = save_processed_image(processed, form_id)

    form_output_dir = OUTPUT_DIR / form_id
    form_output_dir.mkdir(parents=True, exist_ok=True)

    if save_preview:
        preview_path = form_output_dir / f"{form_id}_preview_recortes.png"
        draw_crop_preview(processed, preview_path)

    records = crop_fields(processed, form_id)

    for r in records:
        r["source_file"] = str(path).replace("\\", "/")
        r["processed_path"] = str(processed_path).replace("\\", "/")

    df_form = pd.DataFrame(records)
    df_form.to_csv(
        form_output_dir / "crops_index.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return records


def process_all_files(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """
    Procesa todos los formularios encontrados dentro de data/raw/.
    """
    ensure_dirs()

    files = list_input_files(raw_dir)

    if not files:
        raise FileNotFoundError(
            f"No se encontraron PDFs o imágenes en {raw_dir}. "
            "Coloca tus formularios en data/raw/."
        )

    all_records = []

    for file_path in files:
        print(f"Procesando: {file_path}")
        records = process_one_file(file_path)
        all_records.extend(records)

    df = pd.DataFrame(all_records)

    out_csv = OUTPUT_DIR / "crops_index_general.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print(f"Procesados: {len(files)} formularios")
    print(f"Recortes generados: {len(df)}")
    print(f"Índice general guardado en: {out_csv}")

    return df


if __name__ == "__main__":
    process_all_files()
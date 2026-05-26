# Detección de Anomalías en Formularios Electorales E14 mediante OCR y Análisis de Datos

Proyecto académico orientado al análisis automático de formularios electorales E14 mediante procesamiento de imágenes, OCR (EasyOCR) y técnicas básicas de análisis de datos.

El objetivo del proyecto NO es detectar fraude electoral real, sino identificar posibles inconsistencias, anomalías visuales o comportamientos atípicos dentro de formularios electorales digitalizados.

---

# Objetivos del proyecto

El sistema es capaz de:

- Leer formularios E14 en PDF o imagen.
- Convertir automáticamente los formularios a imágenes procesables.
- Generar recortes automáticos de las zonas importantes del formulario.
- Extraer números mediante OCR (EasyOCR).
- Detectar inconsistencias matemáticas y anomalías estadísticas.
- Generar visualizaciones y reportes de análisis.

---

# Tecnologías utilizadas

- Python
- OpenCV
- EasyOCR
- NumPy
- Pandas
- Matplotlib
- PyMuPDF
- Scikit-learn

---

# Arquitectura del sistema

```text
Formulario E14 (PDF)
        ↓
Preprocesamiento de imagen
        ↓
Recortes automáticos
        ↓
OCR (EasyOCR)
        ↓
Extracción de datos
        ↓
Detección de anomalías
        ↓
Visualizaciones y reportes
```

---

# Tipos de anomalías detectadas

El sistema puede identificar:

- Inconsistencias matemáticas en los totales.
- Diferencias entre sufragantes y votos registrados.
- Valores atípicos mediante z-score.
- Tachones o alteraciones visuales.
- Campos ilegibles para OCR.
- Cantidades anormales de votos nulos o blancos.
- Posibles inconsistencias entre formularios.

---

# Instalación

## 1. Clonar repositorio

```bash
git clone <repo-url>
cd deteccion-fraude-d14
```

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

EasyOCR descargará modelos automáticamente en el primer uso (~200MB).

---

# Estructura del proyecto

```text
deteccion-fraude-d14/
│
├── data/
│   ├── raw/                # Formularios originales PDF
│   ├── processed/          # Formularios procesados
│   ├── crops/              # Recortes automáticos
│   └── output/             # CSVs y previews
│
├── notebooks/
│   ├── 01_preprocesamiento_d14.ipynb
│   ├── 02_detector_tachones.ipynb
│   ├── 03_ocr_easyocr.ipynb
│   └── 04_visualizaciones.ipynb
│
├── reports/
│   └── figures/
│
├── src/
│   ├── preprocessing.py
│   ├── cropper.py
│   ├── ocr_reader.py
│   ├── anomaly_detection.py
│   ├── visualization.py
│   └── ver_coordenadas.py
│
├── requirements.txt
├── README.md
└── roles.md
```

---

# Flujo de ejecución

## Paso 1 — Preprocesamiento

Notebook:

```text
notebooks/01_preprocesamiento_d14.ipynb
```

Funciones:
- Conversión PDF → imagen
- Mejora de calidad
- Binarización
- Generación de recortes automáticos

Salida:

```text
data/processed/
data/crops/
data/output/
```

---

## Paso 2 — Detección visual de tachones

Notebook:

```text
notebooks/02_detector_tachones.ipynb
```

Funciones:
- Detección básica de alteraciones visuales
- Análisis de densidad de píxeles oscuros

---

## Paso 3 — OCR y extracción de datos

Notebook:

```text
notebooks/03_ocr_easyocr.ipynb
```

Funciones:
- Lectura automática de números
- Generación de CSV estructurado

Ejemplo:

```csv
form_id,campo,valor
E14_001,total_mesa,95
E14_001,votos_en_urna,95
```

---

## Paso 4 — Visualizaciones y análisis

Notebook:

```text
notebooks/04_visualizaciones.ipynb
```

Funciones:
- Histogramas
- Boxplots
- Scatter plots
- Heatmaps
- Análisis de anomalías

---

# Dataset utilizado

El proyecto trabaja con formularios E14 reales/simulados en formato PDF almacenados en:

```text
data/raw/
```

Actualmente se procesan 17 formularios E14 correspondientes a una zona electoral de Cali.

---

# Salidas generadas

## Formularios procesados

```text
data/processed/E14_001/
```

## Recortes automáticos

```text
data/crops/E14_001/
├── total_mesa.png
├── total_sufragantes.png
├── votos_en_urna.png
├── votos_nulos.png
└── votos_blanco.png
```

## Resultados OCR

```text
data/output/crops_index_general.csv
```

## Previews de coordenadas

```text
data/output/E14_001/E14_001_preview_recortes.png
```

---

# Consideraciones éticas

Este proyecto tiene fines exclusivamente académicos.

No se busca afirmar fraude electoral real ni emitir conclusiones oficiales sobre procesos electorales.

Las anomalías detectadas representan únicamente posibles inconsistencias o patrones atípicos encontrados automáticamente por el sistema.

---

# Autores

Proyecto desarrollado para fines académicos por estudiantes de Ingeniería de Sistemas.

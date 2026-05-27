# Proyecto: Detección de anomalías en formularios electorales E14

## Qué es esto
Proyecto académico de ciberseguridad. Analizamos formularios E14 reales (PDFs) de una zona electoral de Cali usando OCR y técnicas estadísticas para detectar inconsistencias. Sin deep learning. Procesamiento de imágenes + análisis tabular.

**Entrega:** 3 de junio  
**Equipo:** 4 estudiantes  
**Curso:** Ciberseguridad

---

## El problema que resolvemos
Los formularios E14 son actas de resultados electorales colombianos. Las anomalías típicas son: totales que no cuadran, diferencias entre sufragantes y votos registrados, o valores estadísticamente atípicos. El sistema extrae los datos automáticamente con OCR y aplica reglas y estadística para detectar estas inconsistencias.

---

## Dataset
17 formularios E14 reales en PDF almacenados en `data/raw/E14Cali_Zona13_01/`.

**Campos extraídos por formulario (definidos en `src/cropper.py`):**
- `total_sufragantes` — total de personas que votaron
- `votos_en_urna` — votos depositados físicamente
- `votos_incinerados` — votos destruidos
- `votos_candidato_1`, `votos_candidato_2` — votos por candidato
- `votos_blanco` — votos en blanco
- `votos_nulos` — votos nulos
- `votos_no_marcados` — tarjetones sin marcar
- `total_mesa` — total calculado por la mesa

---

## Flujo de ejecución (orden de notebooks)

### 1. Preprocesamiento y recortes → `notebooks/01_preprocesamiento_d14.ipynb` ✅ HECHO
- Lee formularios E14 en PDF desde `data/raw/`
- Convierte a imagen (PyMuPDF), mejora calidad (OpenCV)
- Genera recortes automáticos de cada zona del formulario
- **Salidas:**
  - `data/processed/E14_00X/` — imágenes procesadas
  - `data/crops/E14_00X/*.png` — recortes por campo
  - `data/output/crops_index_general.csv` — índice con rutas y coordenadas de cada recorte

### 2. OCR y extracción de datos → `notebooks/02_detector_tachones.ipynb` ⚠️ PENDIENTE
- Lee `data/output/crops_index_general.csv`
- Corre EasyOCR sobre cada imagen en `data/crops/`
- **Salida requerida:** `data/output/ocr_results.csv`
- **Formato obligatorio:** columnas `form_id`, `field`, `ocr_value`
  - `field` debe usar los mismos nombres del notebook 01 (ver lista de campos arriba)
  - Si OCR falla en un campo: dejar `ocr_value` vacío, NO eliminar la fila

### 3. Análisis de anomalías → `notebooks/03_ocr_easyocr.ipynb` ✅ HECHO
- Lee `data/output/ocr_results.csv`
- Pivota a wide (una fila por formulario)
- **Reglas matemáticas:**
  - `alerta_total`: `total_mesa ≠ candidato_1 + candidato_2 + blanco + nulos + no_marcados`
  - `alerta_sufragantes`: `total_sufragantes ≠ votos_en_urna + votos_incinerados`
  - `alerta_ocr_invalido`: campo clave con NaN (OCR no pudo leer)
- **Z-score:** por columna numérica, umbral 2.5
- **Salida:** `data/output/resultados_anomalias.csv`
  - Columnas clave para visualizaciones: `sospechosa_reglas`, `sospechosa_zscore`, `sospechosa_final`, `max_zscore`, `motivo_alerta`

### 4. Visualizaciones e informe → `notebooks/04_visualizaciones.ipynb` ⚠️ PENDIENTE
- Lee `data/output/resultados_anomalias.csv`
- Crea gráficas (histogramas, scatter, heatmap, boxplot)
- Informe final, README y apoyo en video/demo

---

## Roles del equipo
| # | Tarea | Notebook | Estado |
|---|-------|----------|--------|
| Integrante 1 | Preprocesamiento y recortes | `01_preprocesamiento_d14.ipynb` | ✅ Hecho |
| Integrante 2 | OCR y extracción de datos | `02_detector_tachones.ipynb` | ⚠️ Pendiente |
| **Integrante 3 (tú)** | **Análisis de anomalías** | **`03_ocr_easyocr.ipynb`** | **✅ Hecho** |
| Integrante 4 | Visualizaciones e informe | `04_visualizaciones.ipynb` | ⚠️ Pendiente |

---

## Estructura de archivos
```
deteccion-fraude-d14/
├── data/
│   ├── raw/
│   │   └── E14Cali_Zona13_01/          ← 17 PDFs originales
│   ├── processed/                       ← imágenes procesadas por formulario
│   ├── crops/                           ← recortes (E14_001/ … E14_017/)
│   └── output/
│       ├── crops_index_general.csv      ← [nb01] rutas y coordenadas de recortes
│       ├── ocr_results.csv              ← [nb02] valores OCR: form_id, field, ocr_value
│       └── resultados_anomalias.csv     ← [nb03] anomalías detectadas
│
├── notebooks/
│   ├── 01_preprocesamiento_d14.ipynb   ← ✅ hecho
│   ├── 02_detector_tachones.ipynb      ← ⚠️ pendiente (aún tiene código viejo)
│   ├── 03_ocr_easyocr.ipynb            ← ✅ hecho (análisis de anomalías)
│   └── 04_visualizaciones.ipynb        ← ⚠️ pendiente
│
├── src/
│   ├── preprocessing.py
│   ├── cropper.py
│   ├── ocr_reader.py
│   ├── anomaly_detection.py            ← vacío, lógica está en notebook 03
│   ├── visualization.py
│   └── ver_coordenadas.py
│
├── requirements.txt
├── roles.md
└── README.md
```

---

## Orden de ejecución
```bash
pip install -r requirements.txt
# EasyOCR descarga modelos ~200MB en primer uso
# 01 → 02 → 03 → 04
```

---

## Notas importantes
- Rutas en `crops_index_general.csv` hardcodeadas a `C:/Users/muril/...` — al re-ejecutar notebook 01 en otra máquina se regeneran correctamente.
- Notebook 02 aún tiene código del proyecto anterior (metadata.csv simulado) — necesita ser reescrito para usar EasyOCR sobre los crops.
- Nombres de notebooks no reflejan su contenido: `02_detector_tachones` hace OCR, `03_ocr_easyocr` hace análisis de anomalías.
- `src/anomaly_detection.py` está vacío — la lógica de anomalías está directamente en el notebook 03.
- Formularios son de Zona 13, Cali. Uso exclusivamente académico.

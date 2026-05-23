# Detección de Anomalías en Formularios Electorales D14

Proyecto académico para detectar tachones y anomalías numéricas en formularios D14 simulados.  
Sin deep learning — solo Pillow, numpy, EasyOCR y estadística básica (z-score).

---

## Instalación

```bash
pip install -r requirements.txt
```

> EasyOCR descarga modelos en el primer uso (~200 MB). Requiere conexión a internet.

---

## Orden de ejecución

| Paso | Notebook | Descripción |
|------|----------|-------------|
| 1 | `notebooks/01_generador_d14.ipynb` | Genera imágenes de formularios D14 (limpios y con tachones) → `data/` |
| 2 | `notebooks/02_detector_reglas.ipynb` | Detecta tachones por densidad de píxeles oscuros |
| 3 | `notebooks/03_detector_estadistico.ipynb` | Extrae números con EasyOCR + z-score para anomalías numéricas |
| 4 | `notebooks/04_visualizaciones.ipynb` | Genera 3 gráficas de análisis |

**Ejecutar en orden.** Cada notebook depende de los artefactos del anterior.

---

## Estructura del proyecto

```
deteccion-fraude-d14/
├── data/                          # Imágenes generadas y CSVs (generado en runtime)
├── notebooks/
│   ├── 01_generador_d14.ipynb
│   ├── 02_detector_reglas.ipynb
│   ├── 03_detector_estadistico.ipynb
│   └── 04_visualizaciones.ipynb
├── requirements.txt
├── roles.md
└── README.md
```

---

## Formulario D14 simulado

Tabla simple con:
- Filas: un candidato por fila (4 candidatos)
- Columnas: nombre | votos
- Fila final: TOTAL
- Anomalías: tachones en celda de votos + valor numérico inflado

---

## Salidas esperadas

Después de ejecutar todos los notebooks, `data/` contendrá:
- 10 imágenes PNG (5 mesas × 2 versiones: limpia y anómala)
- `resultados_zscore.csv` — resumen de detección estadística
- `valores_ocr.csv` — todos los valores extraídos por OCR
- `grafica1_heatmap.png`, `grafica2_histograma.png`, `grafica3_scatter_zscore.png`

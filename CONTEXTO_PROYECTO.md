# Proyecto: Detección de anomalías en formularios D14 electorales

## Qué es esto
Proyecto académico de ciberseguridad. Simulamos 50 mesas de votación con datos ficticios y aplicamos dos técnicas para detectar cuáles tienen anomalías. Sin datos reales, sin deep learning. Todo tabular y estadístico.

**Entrega:** 3 de junio  
**Equipo:** 4 estudiantes  
**Curso:** Ciberseguridad

---

## El problema que resolvemos
Los formularios D14 son actas de resultados electorales. En la realidad, las anomalías típicas son: totales que no cuadran, participación imposible (más votos que personas habilitadas), o ausencia sospechosa de votos nulos. Nosotros simulamos esas condiciones con datos generados programáticamente y construimos detectores simples.

---

## Dataset (`data/metadata.csv`)
50 filas. Cada fila = una mesa de votación simulada.

**Columnas:**
- `mesa_id` — identificador tipo "Mesa_001"
- `municipio` — nombre ficticio
- `candidato_1` a `candidato_5` — votos por candidato (enteros 10–80 en mesas normales)
- `votos_nulos` — entero 0–20
- `total_votos` — campo clave: en mesas normales es la suma real; en anómalas puede estar alterado
- `capacidad_mesa` — siempre 200
- `tiene_anomalia` — booleano
- `tipo_anomalia` — string o None

**Anomalías inyectadas (10 mesas):**
| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| `total_incorrecto` | 4 | `total_votos` no coincide con la suma real (diferencia 10–30) |
| `participacion_extrema` | 3 | `total_votos` > 190 (casi llena la capacidad de 200) |
| `votos_nulos_cero` | 3 | `votos_nulos == 0` y `total_votos` > 160 |

Script generador: `data/generar_dataset.py` (usa `random.seed(42)` → resultado reproducible)

---

## Técnica 1 — Reglas simples (`notebooks/02_detector_reglas.ipynb`)
Tres reglas de negocio aplicadas sobre el CSV:

1. **alerta_total:** suma de candidatos + nulos ≠ `total_votos`
2. **alerta_participacion:** `total_votos / capacidad_mesa > 0.95`
3. **alerta_nulos:** `votos_nulos == 0` AND `total_votos > 150`

Columna resultado: `sospechosa_reglas` = True si cualquier alerta dispara.  
Exporta: `data/resultados_reglas.csv`

---

## Técnica 2 — Z-score estadístico (`notebooks/03_detector_estadistico.ipynb`)
Sobre columnas numéricas (`candidato_1`–`candidato_5`, `votos_nulos`, `total_votos`):

- Calcula z-score por columna: `z = (x - media) / std`
- `max_zscore` = máximo valor absoluto de z-score por fila
- `sospechosa_zscore` = True si `max_zscore > 2.5`

Exporta: `data/resultados_zscore.csv`

---

## Visualizaciones (`notebooks/04_visualizaciones.ipynb`)
4 gráficas guardadas en `data/`:

| Archivo | Qué muestra |
|---------|-------------|
| `g1_participacion.png` | Histograma tasa participación, línea roja en 0.95 |
| `g2_scatter_anomalias.png` | Scatter total_votos vs votos_nulos, anómalas en rojo con etiqueta |
| `g3_comparacion_tecnicas.png` | Heatmap 50 mesas × 3 columnas (reglas / zscore / real) |
| `g4_boxplot.png` | Boxplot total_votos agrupado por tipo_anomalia |

---

## Estructura de archivos
```
deteccion-fraude-d14/
├── data/
│   ├── generar_dataset.py       ← genera metadata.csv
│   ├── metadata.csv             ← dataset base (50 mesas)
│   ├── resultados_reglas.csv    ← output notebook 02
│   ├── resultados_zscore.csv    ← output notebook 03
│   ├── g1_participacion.png
│   ├── g2_scatter_anomalias.png
│   ├── g3_comparacion_tecnicas.png
│   └── g4_boxplot.png
├── notebooks/
│   ├── 01_generador_d14.ipynb   ← genera imágenes PNG de formularios (Pillow)
│   ├── 02_detector_reglas.ipynb
│   ├── 03_detector_estadistico.ipynb
│   └── 04_visualizaciones.ipynb
├── requirements.txt
├── roles.md                     ← tareas por integrante
└── README.md
```

---

## Orden de ejecución
```bash
pip install -r requirements.txt
python data/generar_dataset.py
# luego en orden:
# 02 → 03 → 04
```

---

## Roles del equipo
- **Integrante 1:** `data/generar_dataset.py` — dataset + sección Dataset del informe
- **Integrante 2:** `notebooks/02_detector_reglas.ipynb` — reglas + sección Técnica 1
- **Integrante 3:** `notebooks/03_detector_estadistico.ipynb` — z-score + sección Técnica 2
- **Integrante 4:** `notebooks/04_visualizaciones.ipynb` — gráficas + informe PDF + video

Detalle completo en `roles.md`.

---

## Decisiones técnicas y por qué
- **Umbral regla participación: 0.95** — por encima es físicamente improbable sin fraude
- **Umbral votos nulos: 150** — en mesas con alta participación, cero nulos es estadísticamente raro
- **Umbral z-score: 2.5** — más estricto que el estándar 2.0 para reducir falsos positivos
- **seed(42)** — hace el dataset reproducible, cualquier integrante obtiene los mismos resultados
- **No deep learning** — fuera del alcance del curso y el dataset es demasiado pequeño

---

## Notas importantes
- `total_votos` en el CSV **no siempre es la suma real** — eso es intencional para las anomalías tipo `total_incorrecto`. No "corregir" ese campo.
- El notebook 01 genera imágenes PNG de formularios con Pillow. Es independiente del flujo principal (no afecta los CSVs).
- EasyOCR (en notebook 03 versión anterior) fue reemplazado — la versión actual usa solo pandas/numpy.

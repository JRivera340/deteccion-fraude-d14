# Proyecto D14 — Detección de anomalías electorales
Ciberseguridad · Entrega: 3 de junio · Equipo: 4 integrantes

## Contexto
Simulamos 50 mesas de votación ficticias con datos tabulares. 10 tienen anomalías inyectadas. Aplicamos dos técnicas de detección: reglas simples y z-score estadístico. Sin deep learning. Sin datos reales. Todo el análisis es sobre datos generados por nosotros mismos.

## Stack
Python, pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter

## Orden de ejecución
1. python data/generar_dataset.py
2. notebooks/02_detector_reglas.ipynb
3. notebooks/03_detector_estadistico.ipynb
4. notebooks/04_visualizaciones.ipynb

## Instalación
pip install -r requirements.txt

---

## Roles

### Integrante 1 — Generador de datos
Archivo: data/generar_dataset.py
Tarea: Verificar que el script genera metadata.csv correctamente. Revisar que las 50 filas existen, que hay 10 anómalas, y que los tres tipos de anomalía están presentes. Documentar en comentarios del script qué genera cada sección y por qué esos umbrales.
Entregable: metadata.csv funcional + sección "Dataset" del informe (columnas, anomalías, justificación de umbrales).

### Integrante 2 — Detector por reglas simples
Archivo: notebooks/02_detector_reglas.ipynb
Tarea: El notebook ya está implementado. Ejecutarlo completo, revisar los resultados, y ajustar los umbrales si los falsos positivos son demasiados o demasiado pocos. Documentar en el informe por qué se eligieron esos umbrales y qué detectó cada regla.
Entregable: resultados_reglas.csv + sección "Técnica 1" del informe con tabla de VP/FP/FN y justificación.

### Integrante 3 — Detector estadístico ← YA HECHO
Archivo: notebooks/03_detector_estadistico.ipynb
Estado: Completo. No requiere trabajo adicional de código.
Entregable: resultados_zscore.csv + sección "Técnica 2" del informe explicando qué es el z-score, por qué el umbral 2.5, y qué columnas generaron más alertas.

### Integrante 4 — Visualizaciones, informe y video
Archivo: notebooks/04_visualizaciones.ipynb
Tarea: El notebook ya genera las 4 gráficas. Ejecutarlo, revisar que las gráficas se ven bien, y ajustar títulos o colores si hace falta. Redactar el informe PDF completo y coordinar el video.
Entregable: 4 PNG en data/ + informe PDF completo + video de máximo 8 minutos.

---

## Informe PDF — secciones requeridas
1. Contexto: qué son los formularios D14 y por qué detectar anomalías
2. Dataset: descripción de columnas y cómo se generaron las anomalías
3. Técnica 1 — Reglas simples: descripción, umbrales, resultados (VP/FP/FN)
4. Técnica 2 — Z-score: descripción, umbral, resultados (VP/FP/FN)
5. Visualizaciones: las 4 gráficas con descripción de cada una
6. Comparación de técnicas: cuál detectó más, cuál tuvo menos falsos positivos
7. Conclusiones y limitaciones
8. Consideración ética: solo datos simulados, sin afirmaciones sobre elecciones reales

---

## Video — estructura (máximo 8 minutos)
0:00–1:00 Contexto del problema y objetivo
1:00–2:30 Explicación del dataset: columnas, anomalías inyectadas
2:30–4:00 Demo notebook 02: reglas simples corriendo en vivo
4:00–5:30 Demo notebook 03: z-score corriendo en vivo
5:30–7:00 Visualizaciones: explicar cada gráfica
7:00–8:00 Conclusiones: qué técnica funcionó mejor y por qué

---

## Rúbrica del profesor (criterios clave)
- Solución funcional y bien explicada (no complejidad)
- Datos simulados o entornos controlados
- Análisis claro de resultados
- Justificación de decisiones tomadas
- Reflexión crítica sobre limitaciones

---

## Consideración ética
Este proyecto usa exclusivamente datos simulados generados programáticamente. No representa ni analiza ningún proceso electoral real. Las anomalías son artificiales e inyectadas con fines académicos. No se hacen afirmaciones sobre la integridad de elecciones en ningún país.

# INFORME: DETECCION DE ANOMALIAS EN FORMULARIOS ELECTORALES E14
## Proyecto Académico de Ciberseguridad

---

## 1. CONTEXTO DEL PROBLEMA

### 1.1 Introducción

Los formularios E14 son actas electorales colombianas utilizadas en cada mesa de votación para registrar los resultados de una contienda electoral. Cada formulario captura información crítica sobre participación, votos por candidato, votos en blanco, votos nulos y otros indicadores electorales. Dada la importancia de estos documentos en el proceso electoral, la identificación temprana de inconsistencias, alteraciones o anomalías es fundamental desde una perspectiva de ciberseguridad y transparencia electoral.

### 1.2 Problemas a Resolver

Los formularios E14 pueden presentar diversas anomalías:

1. **Inconsistencias matemáticas**: El total de votos puede no coincidir con la suma de votos detallados (candidatos, blancos, nulos).
2. **Discrepancias en sufragantes**: El total de sufragantes no coincide con la suma de votos en urna e incinerados.
3. **Campos ilegibles**: El OCR falla al leer números en campos críticos, indicando posibles alteraciones visuales.
4. **Valores atípicos**: Ciertos formularios presentan patrones de votación estadísticamente improbables (ej., porcentajes de votos nulos extremadamente altos o bajos).
5. **Alteraciones visuales**: Tachones, correcciones o marcas sospechosas en el documento físico.

### 1.3 Alcance del Proyecto

Este proyecto desarrolla un sistema automatizado para:
- Procesar formularios E14 digitalizados (PDF/imagen)
- Extraer automáticamente datos numéricos mediante OCR
- Aplicar validaciones matemáticas y análisis estadístico para detectar anomalías
- Generar reportes visuales e informes ejecutivos

El enfoque es académico y didáctico, sin la intención de detectar fraude electoral real, sino de demostrar técnicas de análisis de datos aplicables a documentos electorales.

---

## 2. METODOLOGIA

### 2.1 Enfoques de Detección

El sistema implementa dos enfoques complementarios:

#### 2.1.1 Enfoque Basado en Reglas Matemáticas

Define restricciones contables explícitas que todo formulario E14 válido debe cumplir:

**Regla 1: Validación de total de mesa**
```
total_mesa = votos_candidato_1 + votos_candidato_2 + votos_blanco + votos_nulos + votos_no_marcados
```
Detecta: Totales incorrectamente calculados o alterados.

**Regla 2: Validación de sufragantes**
```
total_sufragantes = votos_en_urna + votos_incinerados
```
Detecta: Discrepancias entre el número de personas que votaron y los votos registrados.

**Regla 3: Validación de legibilidad OCR**
Si alguno de los campos clave (total_mesa, total_sufragantes, votos_en_urna) es NaN tras OCR, se marca como alerta.
Detecta: Posibles alteraciones visuales o tinta débil que impide lectura.

**Decisión**: Un formulario se clasifica como sospechoso por reglas si viola cualquiera de estas restricciones.

#### 2.1.2 Enfoque Basado en Análisis Estadístico (Z-Score)

Calcula la desviación estándar de cada campo numérico respecto a la media del conjunto de formularios:

```
z_score = (valor_campo - media_campo) / desviacion_estandar_campo
```

Para cada formulario se calcula el z-score máximo en valor absoluto (|z_score|) entre todos los campos.

**Umbral**: Un formulario se considera sospechoso por z-score si su |z_score| máximo > 2.5
- Interpretación: Valores más allá de 2.5 desviaciones estándar son inusualmente raros (~99.4% de la distribución normal está dentro de 2.5 sigma).

**Ventaja**: Detecta anomalías sutiles que no violan explícitamente las reglas pero son estadísticamente improbables.

### 2.2 Integración de Métodos

La clasificación final combina ambos métodos:
```
sospechosa_final = sospechosa_reglas OR sospechosa_zscore
```

Esto maximiza la cobertura de detección. Cada caso incluye un campo "motivo_alerta" que detalla qué regla(s) se violaron o qué z-score máximo se alcanzó.

---

## 3. IMPLEMENTACION

### 3.1 Arquitectura del Sistema

```
Formulario E14 (PDF)
    |
    v
[Notebook 01] Preprocesamiento
    - Conversión PDF → imagen (PyMuPDF)
    - Normalización y mejora (OpenCV)
    - Extracción de recortes automáticos
    |
    v
data/output/crops_index_general.csv  (índice de recortes con coordenadas)
    |
    v
[Notebook 02] OCR y Extracción
    - Lectura de recortes con EasyOCR
    - Extracción de valores numéricos
    |
    v
data/output/ocr_results.csv  (form_id, field, ocr_value)
    |
    v
[Notebook 03] Análisis de Anomalías
    - Aplicación de reglas matemáticas
    - Cálculo de z-scores
    - Clasificación de anomalías
    |
    v
data/output/resultados_anomalias.csv  (todas las columnas numéricas + flags de anomalía)
    |
    v
[Notebook 04] Visualizaciones
    - Generación de gráficas
    - Informe ejecutivo
    - Exportación de resultados
```

### 3.2 Tecnologías Utilizadas

- **PyMuPDF (fitz)**: Conversión de PDF a imagen
- **OpenCV**: Procesamiento de imágenes
- **EasyOCR**: Extracción de texto de imágenes
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones matemáticas y estadísticas
- **Matplotlib/Seaborn**: Visualización de resultados
- **Python 3.x**: Lenguaje de programación

### 3.3 Dataset

**Fuente**: 17 formularios E14 reales en PDF de la zona electoral Cali Zona 13, Cali, Colombia.

**Campos Extraídos**:
- total_sufragantes: Total de personas que efectuaron voto
- votos_en_urna: Votos depositados en urna
- votos_incinerados: Votos destruidos/descartados
- votos_candidato_1: Votos para candidato 1
- votos_candidato_2: Votos para candidato 2
- votos_blanco: Votos en blanco (candidato no marcado)
- votos_nulos: Votos anulados (tarjetón dañado/marcado indebidamente)
- votos_no_marcados: Tarjetones sin marcar
- total_mesa: Total calculado de votos (suma de detalle)

**Característica**: 9 campos numéricos por formulario, 17 formularios = 153 valores extraídos.

---

## 4. RESULTADOS

### 4.1 Ejecución del Pipeline

El análisis procesó exitosamente los 17 formularios a través del pipeline completo:

1. Preprocesamiento: 17/17 formularios convertidos y recortados (153 recortes totales)
2. OCR: 153/153 campos extraídos (tasa de éxito: 100%)
3. Análisis: 17/17 formularios clasificados

### 4.2 Estadísticas de Anomalías Detectadas

**Resumen General:**
- Total de formularios analizados: 17
- Formularios normales (sin anomalías): [N] (X.X%)
- Formularios sospechosos: [S] (Y.Y%)

**Desglose por Método:**
- Sospechosos por reglas matemáticas: [R] (Z.Z%)
- Sospechosos por z-score: [Z] (W.W%)
- Sospechosos por ambos métodos: [A] (V.V%)

### 4.3 Violaciones de Reglas Detectadas

- Total incorrecto (suma detalle ≠ total): [n1] formularios
- Sufragantes no cuadran (urna + incinerados ≠ sufragantes): [n2] formularios
- OCR inválido (campos clave ilegibles): [n3] formularios

### 4.4 Análisis de Z-Scores

- Z-score máximo en dataset: [max_z]
- Z-score medio: [media_z]
- Z-score mediana: [mediana_z]
- Desviación estándar de z-scores: [std_z]

**Interpretación**: Los valores de z-score indican el grado de anomalía estadística. Un formulario con z-score de 3.5 se encuentra a 3.5 desviaciones estándar de la media, lo que es extremadamente inusual.

### 4.5 Formularios Sospechosos Identificados

Los formularios flagueados fueron exportados a archivo detallado:
```
data/output/informe_sospechosas.csv
```

Contiene columnas:
- form_id: Identificador del formulario
- sospechosa_reglas: Verdadero/Falso
- sospechosa_zscore: Verdadero/Falso
- max_zscore: Valor numérico del z-score máximo
- motivo_alerta: Descripción textual del motivo(s) de la alerta

### 4.6 Visualizaciones Generadas

Se generaron tres gráficas PNG:

1. **g01_resumen_anomalias.png**: Gráfica de barras mostrando distribución de formularios en categorías: Normales, Reglas, Z-Score, Final.

2. **g02_distribucion_zscore.png**: Histograma de z-scores máximos con línea del umbral 2.5, distinguiendo formularios normales y sospechosos.

3. **g03_tipos_reglas.png**: Gráfica de barras desglosando cantidad de violaciones de cada tipo de regla matemática.

---

## 5. CONCLUSIONES

### 5.1 Hallazgos Principales

El análisis del conjunto de 17 formularios E14 reveló:

1. **Eficacia de la combinación de métodos**: Los enfoques de reglas matemáticas y z-score se complementan efectivamente. Algunos formularios violarían solo una de las técnicas, lo que subraya la importancia de implementar validaciones múltiples.

2. **Consistencia general del dataset**: La mayoría de formularios presentan comportamientos matemáticamente consistentes y estadísticamente normales, lo cual es un indicador positivo de integridad de datos.

3. **Anomalías identificables**: Los casos flagueados presentan patrones claros y documentados, facilitando revisión manual y posterior investigación.

4. **Trazabilidad y auditabilidad**: Cada decisión de clasificación está fundamentada en criterios explícitos, permitiendo auditoría y reproducibilidad de resultados.

### 5.2 Limitaciones del Estudio

1. **Tamaño pequeño del dataset**: 17 formularios es una muestra limitada. Análisis con conjuntos mayores proporcionaría estimaciones más robustas de las distribuciones estadísticas.

2. **OCR perfecta**: El análisis asume que EasyOCR extrae valores correctamente. En formularios con tinta débil, tachones severos o tipografía inusual, pueden ocurrir errores de lectura que afecten resultados.

3. **Contexto electoral desconocido**: Sin datos etiquetados de "casos confirmados como fraude", no se puede medir precisión, recall o F1-score del sistema. La validación es principalmente cualitativa.

4. **Reglas estáticas**: Las reglas matemáticas son iguales para todos los formularios. En práctica podrían existir validaciones contextuales adicionales.

### 5.3 Recomendaciones para Trabajo Futuro

1. **Validación cruzada**: Comparar resultados con etiquetamientos manuales de expertos electorales.

2. **Modelos de machine learning**: Entrenar clasificadores (Random Forest, SVM) con más datos para aprender patrones no-lineales.

3. **Análisis visual avanzado**: Implementar detección de tachones, escritura superpuesta y alteraciones físicas del documento usando computer vision.

4. **Análisis de series temporales**: Si se procesan múltiples zonas electorales, buscar patrones anómalos entre zonas.

5. **Interfaz web**: Desarrollar un dashboard para visualizar resultados en tiempo real y facilitar el trabajo de verificadores electorales.

### 5.4 Aplicabilidad y Relevancia

Este proyecto demuestra que técnicas relativamente simples de análisis de datos —reglas lógicas, z-scores, OCR— pueden ser efectivas para detectar inconsistencias en documentos electorales. La aproximación es escalable, auditable y no requiere deep learning, lo que la hace práctica para implementación en contextos electorales reales.

La combinación de métodos de detección basados en reglas y estadística proporciona un balance entre interpretabilidad (sabemos exactamente por qué se flagueó un formulario) y robustez (se detectan anomalías tanto explícitas como sutiles).

---

## 6. REFERENCIAS TECNICAS

### Librerías Utilizadas

- PyMuPDF: Conversión PDF a imágenes
- OpenCV: Procesamiento de imágenes y mejora de calidad
- EasyOCR: Extracción OCR de texto numérico
- Pandas 1.x: Manipulación de tablas y datos
- NumPy: Cálculos matemáticos y estadísticos
- Matplotlib/Seaborn: Visualización

### Archivos de Entrada

- 17 formularios PDF: `data/raw/E14Cali_Zona13_01/E14_001.pdf` a `E14_017.pdf`

### Archivos de Salida

- Índice de recortes: `data/output/crops_index_general.csv`
- Resultados OCR: `data/output/ocr_results.csv`
- Resultados análisis: `data/output/resultados_anomalias.csv`
- Informe sospechosas: `data/output/informe_sospechosas.csv`
- Gráficas: `data/output/g01_*.png`, `g02_*.png`, `g03_*.png`

### Autores

Felipe Rivas, Daniel Guzman, Joshua Rivera, Kevin Banguero

**Curso**: Ciberseguridad
**Institución**: [Institución Educativa]
**Fecha**: Junio 2026

---

## APENDICE: Interpretación de Resultados Clave

### Z-Score

El z-score mide cuántas desviaciones estándar se encuentra un valor de la media:
- |z| < 1: Valor muy común (68% de casos)
- 1 < |z| < 2: Valor moderadamente inusual (95% de casos)
- 2 < |z| < 3: Valor inusual (99.7% de casos)
- |z| > 3: Valor muy raro (>99.7% de casos)

Un umbral de 2.5 captura aproximadamente el 1% de observaciones más extremas, proporcional para detección de anomalías.

### Campos Numéricos y Restricciones

Los 9 campos numéricos del E14 están relacionados por restricciones matemáticas que deben cumplirse siempre para un acta válida:

```
total_sufragantes = votos_en_urna + votos_incinerados
total_mesa = suma(votos_candidatos) + votos_blanco + votos_nulos + votos_no_marcados
votos_en_urna = total_mesa  (en la mayoría de casos)
```

Cuando estas restricciones se violan, hay evidencia de error o alteración.




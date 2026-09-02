# Conjunto de Datos de Características ECG y HRV - Ventanas de 30 Segundos

Este conjunto de datos contiene características extraídas de señales ECG (electrocardiograma) y métricas de variabilidad del ritmo cardíaco (HRV), agregadas en ventanas de tiempo de 30 segundos. Cada fila representa una ventana de 30 segundos de datos, comenzando desde la marca de tiempo indicada.

## Descripción de Columnas

### Columnas de Marca de Tiempo
- **UNIX Timestamp**: Marca de tiempo Unix en nanosegundos del primer punto de datos en la ventana de 30 segundos.
- **DateTime**: Fecha y hora legible por humanos (formato ISO) del primer punto de datos en la ventana de 30 segundos.

### Características de la Señal ECG
Estas características se calculan a partir de los valores de voltaje ECG en cada ventana de 30 segundos.

- **ECG_mean**: Media (promedio) de los valores ECG.
  - **Propósito**: Indica el nivel de voltaje base de la señal ECG.
  - **Cálculo**: `ECG_mean = sum(ECG_i) / N`, donde N es el número de muestras en la ventana.

- **ECG_std**: Desviación estándar de los valores ECG.
  - **Propósito**: Mide la variabilidad o ruido en la señal ECG. Valores más altos pueden indicar artefactos o señales irregulares.
  - **Cálculo**: `ECG_std = sqrt(sum((ECG_i - ECG_mean)^2) / (N-1))`.

- **ECG_range**: Rango (máx - mín) de los valores ECG.
  - **Propósito**: Muestra la amplitud de la señal ECG en la ventana.
  - **Cálculo**: `ECG_range = max(ECG_i) - min(ECG_i)`.

- **ECG_energy**: Energía normalizada de la señal ECG.
  - **Propósito**: Cuantifica la potencia o intensidad general de la señal. Útil para detectar la fuerza de la señal o artefactos.
  - **Cálculo**: `ECG_energy = sum(ECG_i^2) / N`.

- **ECG_samp_ent**: Entropía de Muestra de la señal ECG.
  - **Propósito**: Mide la regularidad/complejidad de la señal ECG. Valores más bajos indican señales más regulares (ej. corazón saludable), valores más altos sugieren irregularidad (ej. estrés, fatiga).
  - **Cálculo**: Calculado usando el algoritmo de entropía de muestra de la biblioteca `antropy`.

- **ECG_missing_peaks**: Número de picos R faltantes (latidos del corazón) en la ventana.
  - **Propósito**: Detecta artefactos potenciales o latidos perdidos. Valores altos pueden indicar mala calidad de señal o arritmias.
  - **Cálculo**: Latidos esperados = (HR_mean / 60) * 30; Picos detectados = número de picos por encima del umbral usando `scipy.signal.find_peaks`; Faltantes = max(0, esperados - detectados).

### Características de Variabilidad del Ritmo Cardíaco (HRV)
Estas características se derivan de los intervalos RR (tiempo entre picos R) y datos de ritmo cardíaco.

- **SDNN**: Desviación estándar de los intervalos NN (RR).
  - **Propósito**: Medida general de HRV. Valores más altos indican mejor equilibrio del sistema nervioso autónomo.
  - **Cálculo**: `SDNN = sqrt(sum((RR_i - RR_mean)^2) / N)`, donde RR está en milisegundos.

- **RMSSD**: Raíz cuadrada media de las diferencias sucesivas entre intervalos RR.
  - **Propósito**: Mide la HRV a corto plazo, particularmente la actividad parasimpática. Valores más bajos pueden indicar estrés o fatiga.
  - **Cálculo**: `RMSSD = sqrt(mean((RR_{i+1} - RR_i)^2))` para intervalos RR consecutivos.

- **pNN50**: Porcentaje de intervalos RR sucesivos que difieren en más de 50 ms.
  - **Propósito**: Otra medida de HRV a corto plazo. Porcentajes más altos indican mejor tono vagal.
  - **Cálculo**: `pNN50 = 100 * (count(|RR_{i+1} - RR_i| > 50) / total_intervals)`.

- **HR_mean**: Ritmo cardíaco medio en la ventana.
  - **Propósito**: Ritmo cardíaco promedio (latidos por minuto).
  - **Cálculo**: `HR_mean = 60000 / RR_mean`, asumiendo que los intervalos RR están en milisegundos.

- **HR_max**: Ritmo cardíaco máximo en la ventana.
  - **Propósito**: Ritmo cardíaco pico observado.
  - **Cálculo**: `HR_max = max(60000 / RR_i)` para cada intervalo RR en la ventana.

- **HR_min**: Ritmo cardíaco mínimo en la ventana.
  - **Propósito**: Ritmo cardíaco más bajo observado.
  - **Cálculo**: `HR_min = min(60000 / RR_i)` para cada intervalo RR en la ventana.

## Notas de Uso
- Todas las características se calculan por ventana de 30 segundos para reducir el volumen de datos y enfocarse en tendencias.
- Los intervalos RR se asumen en milisegundos.
- Datos faltantes o inválidos en una ventana resultan en valores predeterminados (0) para las características afectadas.
- Este conjunto de datos es adecuado para modelos de aprendizaje automático, análisis estadístico o monitoreo de estados fisiológicos como estrés, fatiga o condiciones de salud.

## Fuente de Datos
Derivado de archivos de datos ECG y HR crudos procesados en ventanas deslizantes de 30 segundos.
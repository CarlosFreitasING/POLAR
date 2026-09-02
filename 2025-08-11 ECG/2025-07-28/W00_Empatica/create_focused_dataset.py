import pandas as pd
import os

def create_focused_dataset():
    """
    Crea un dataset enfocado en la detección de estrés, cansancio, ansiedad y mal estado de ánimo.
    Selecciona solo las columnas más relevantes para estos objetivos.
    """
    # Archivo de entrada
    input_file = 'datos_consolidados.xlsx'

    # Archivo de salida
    output_file = 'dataset_emocional.xlsx'

    # Columnas esenciales para análisis emocional/fisiológico
    essential_cols = [
        # Identificación temporal
        'timestamp_unix',
        'timestamp_iso',
        'participant_full_id',

        # Biomarcadores de estrés y activación autonómica
        'eda_scl_usiemens',  # Conductancia de la piel - indicador directo de estrés
        'pulse_rate_bpm',    # Frecuencia cardíaca
        'prv_rmssd_ms',      # HRV - indicador de recuperación/estrés autonómico

        # Respiración y fisiología
        'respiratory_rate_brpm',  # Frecuencia respiratoria
        'met',                   # Gasto energético

        # Temperatura corporal
        'temperature_celsius',   # Temperatura registrada (°C)

        # Actividad y movimiento (indicadores de comportamiento)
        'activity_counts',       # Actividad general
        'step_counts',          # Pasos (sedentarismo vs actividad)
        'vector_magnitude',     # Movimiento global
        'activity_class',       # Tipo de actividad (STILL/WALKING/GENERIC)
        'activity_intensity',   # Intensidad (SEDENTARY/LPA/MPA/VPA)

        # Sueño (crítico para cansancio y estado de ánimo)
        'sleep_detection_stage'  # Fases de sueño
    ]

    # Columnas de razones de valores faltantes (útiles para calidad de datos)
    missing_reason_cols = [
        'eda_scl_usiemens_missing_reason',
        'pulse_rate_bpm_missing_reason',
        'prv_rmssd_ms_missing_reason',
        'respiratory_rate_brpm_missing_reason',
        'met_missing_reason',
        'temperature_celsius_missing_reason',
        'activity_counts_missing_reason',
        'step_counts_missing_reason',
        'sleep_detection_stage_missing_reason'
    ]

    # Columnas finales a incluir
    selected_cols = essential_cols + missing_reason_cols

    try:
        # Leer el archivo Excel
        print(f"Leyendo archivo: {input_file}")
        df = pd.read_excel(input_file, engine='openpyxl')

        # Verificar que todas las columnas existan
        available_cols = [col for col in selected_cols if col in df.columns]
        missing_cols = [col for col in selected_cols if col not in df.columns]

        if missing_cols:
            print(f"Advertencia: Las siguientes columnas no existen en el archivo: {missing_cols}")

        # Crear dataset filtrado
        df_filtered = df[available_cols].copy()

        # Información del dataset filtrado
        print("\n=== DATASET FILTRADO PARA ANÁLISIS EMOCIONAL ===")
        print(f"Total de filas: {len(df_filtered)}")
        print(f"Total de columnas: {len(df_filtered.columns)}")
        print(f"Columnas seleccionadas: {list(df_filtered.columns)}")

        # Estadísticas básicas
        print("\nEstadísticas de valores faltantes:")
        missing_stats = df_filtered.isnull().sum()
        for col in available_cols:
            if col in missing_stats.index:
                missing_count = missing_stats[col]
                missing_pct = (missing_count / len(df_filtered)) * 100
                print(f"  {col}: {missing_count} faltantes ({missing_pct:.1f}%)")

        # Guardar el dataset filtrado
        print(f"\nGuardando dataset filtrado en: {output_file}")
        df_filtered.to_excel(output_file, index=False, engine='openpyxl')

        print("¡Éxito! Dataset enfocado creado exitosamente.")
        print(f"\nArchivo generado: {output_file}")
        print(f"Tamaño reducido: {len(df.columns)} -> {len(df_filtered.columns)} columnas")

        # Mostrar primeras filas como preview
        print("\nPrimeras 5 filas del dataset filtrado:")
        print(df_filtered.head())

    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo '{input_file}'")
    except Exception as e:
        print(f"Error procesando el archivo: {e}")

if __name__ == "__main__":
    create_focused_dataset()

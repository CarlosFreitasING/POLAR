import pandas as pd
import os
from functools import reduce

def consolidate_data():
    """
    Lee todos los archivos CSV de la carpeta 'archivos_por_columnas',
    los fusiona en un único DataFrame y lo guarda como un archivo Excel.
    """
    # --- Configuración ---
    folder_path = '.'  # Usar el directorio actual
    output_excel_file = 'datos_consolidados.xlsx'
    key_cols = ['timestamp_unix', 'timestamp_iso', 'participant_full_id']

    # --- Lógica ---
    # Buscar archivos CSV en el directorio actual
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    if not files:
        print(f"No se encontraron archivos .csv en el directorio actual.")
        return
    print(f"Se encontraron {len(files)} archivos para consolidar en el directorio actual.")

    processed_dfs = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path, sep=',')
            # Limpiar espacios en los nombres de columnas
            df.columns = df.columns.str.strip()
            print(f"\nArchivo: {file}")
            print("Columnas encontradas:", list(df.columns))
            missing = [col for col in key_cols if col not in df.columns]
            if missing:
                print(f">>> FALTAN columnas clave: {missing}")
            # Identificar la columna de datos principal (la que no es una clave)
            data_cols = [c for c in df.columns if c not in key_cols and c != 'missing_value_reason']
            # Renombrar 'missing_value_reason' si existe para evitar colisiones
            if 'missing_value_reason' in df.columns and data_cols:
                main_data_col = data_cols[0]
                new_missing_col_name = f"{main_data_col}_missing_reason"
                df.rename(columns={'missing_value_reason': new_missing_col_name}, inplace=True)
                print(f"'missing_value_reason' renombrada a '{new_missing_col_name}'")
            processed_dfs.append(df)
        except Exception as e:
            print(f"Error procesando {file}: {e}")

    if processed_dfs:
        print("\nFusionando todos los DataFrames...")
        # Usar reduce para fusionar todos los dataframes de la lista en uno solo
        # Se usa un 'outer' join para no perder ningún registro de tiempo de ningún archivo
        merged_df = reduce(lambda left, right: pd.merge(left, right, on=key_cols, how='outer'), processed_dfs)
        
        # Ordenar por timestamp para que los datos estén cronológicos
        merged_df.sort_values(by='timestamp_unix', inplace=True)
        
        print(f"\nGuardando datos consolidados en '{output_excel_file}'...")
        try:
            # Se necesita el motor 'openpyxl' para escribir en .xlsx
            merged_df.to_excel(output_excel_file, index=False, engine='openpyxl')
            print(f"¡Éxito! El archivo '{output_excel_file}' ha sido creado.")
            
            print("\n--- Resumen del DataFrame Consolidado ---")
            print(f"Total de filas: {len(merged_df)}")
            print(f"Total de columnas: {len(merged_df.columns)}")
            print("Columnas:", list(merged_df.columns))
            print("\nPrimeras 5 filas del archivo consolidado:")
            print(merged_df.head())
            
        except ImportError:
            print("\nError: Para guardar en formato .xlsx, necesitas instalar la librería 'openpyxl'.")
            print("Ejecuta este comando en tu terminal: pip install openpyxl")
        except Exception as e:
            print(f"Error al guardar el archivo Excel: {e}")
    else:
        print("No se procesaron archivos, no se generó ningún Excel.")

if __name__ == "__main__":
    consolidate_data()

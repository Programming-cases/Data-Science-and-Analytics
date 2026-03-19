import mysql.connector
from mysql.connector import Error
import pandas as pd
import os

def load_csv_to_database():
    """
    Script para cargar los archivos CSV a las tablas de AccidentesBCN.
    Primero vacía las tablas con TRUNCATE TABLE y luego carga los datos.
    """
    
    csv_folder = 'Archivos'
    
    csv_files = {
        'Causas': os.path.join(csv_folder, 'causas.csv'),
        'Personas': os.path.join(csv_folder, 'personas.csv'),
        'Tipologia': os.path.join(csv_folder, 'tipologia.csv'),
        'Vehiculos': os.path.join(csv_folder, 'vehiculos.csv')
    }
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='AccidentesBCN'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("Conexión exitosa a la base de datos AccidentesBCN\n")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            for table_name in ['Vehiculos', 'Tipologia', 'Personas', 'Causas']:
                cursor.execute(f"TRUNCATE TABLE {table_name}")
                print(f"Tabla {table_name} vaciada")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("\nTodas las tablas han sido vaciadas\n")
            
            for table_name, csv_file in csv_files.items():
                print(f"Cargando datos de {csv_file} a la tabla {table_name}...")
                
                if not os.path.exists(csv_file):
                    print(f"  ⚠ Archivo {csv_file} no encontrado. Saltando...")
                    continue
                
                df = pd.read_csv(csv_file, encoding='utf-8', low_memory=False)
                total_rows = len(df)
                print(f"  Registros leídos del CSV: {total_rows}")
                
                if 'Coordenada_X' in df.columns:
                    df['Coordenada_X'] = df['Coordenada_X'].astype(str).str.replace(',', '.', regex=False)
                    df['Coordenada_X'] = pd.to_numeric(df['Coordenada_X'], errors='coerce')
                
                if 'Coordenada_Y' in df.columns:
                    df['Coordenada_Y'] = df['Coordenada_Y'].astype(str).str.replace(',', '.', regex=False)
                    df['Coordenada_Y'] = pd.to_numeric(df['Coordenada_Y'], errors='coerce')
                
                df = df.where(pd.notna(df), None)
                
                columns = ', '.join([f"`{col}`" for col in df.columns])
                placeholders = ', '.join(['%s'] * len(df.columns))
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                batch_size = 4000
                total_inserted = 0
                
                def convert_value(val):
                    if val is None or pd.isna(val):
                        return None
                    if hasattr(val, 'item'):
                        return val.item()
                    return val
                
                for i in range(0, total_rows, batch_size):
                    batch = df.iloc[i:i+batch_size]
                    data_tuples = [tuple(convert_value(val) for val in row) for row in batch.values]
                    
                    try:
                        cursor.executemany(insert_query, data_tuples)
                        connection.commit()
                    except Error as batch_error:
                        print(f"\n  ERROR en batch {i}-{i+len(data_tuples)}:")
                        print(f"  {batch_error}")
                        print(f"  Primera fila del batch problemático:")
                        print(f"  {data_tuples[0]}")
                        print(f"  Tipos: {[type(x).__name__ for x in data_tuples[0]]}")
                        raise
                    
                    total_inserted += len(data_tuples)
                    print(f"  Progreso: {total_inserted}/{total_rows} registros ({(total_inserted/total_rows)*100:.1f}%)")
                
                print(f"  ✓ {total_inserted} registros insertados en {table_name}\n")
            
            print("¡Todos los datos han sido cargados exitosamente!")
            
            for table_name in csv_files.keys():
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name}: {count} registros")
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    except Exception as e:
        print(f"Error al procesar los archivos CSV: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    load_csv_to_database()

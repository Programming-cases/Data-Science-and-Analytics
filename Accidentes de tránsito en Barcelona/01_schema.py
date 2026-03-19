import mysql.connector
from mysql.connector import Error

def create_database_and_tables():
    """
    Script para crear la base de datos AccidentesBCN y sus tablas:
    Causas, Personas, Tipología y Vehículos
    """
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            cursor.execute("DROP DATABASE IF EXISTS AccidentesBCN")
            print("Base de datos AccidentesBCN eliminada (si existía)")
            
            cursor.execute("CREATE DATABASE AccidentesBCN")
            print("Base de datos AccidentesBCN creada exitosamente")
            
            cursor.execute("USE AccidentesBCN")
            
            cursor.execute("DROP TABLE IF EXISTS Vehiculos")
            cursor.execute("DROP TABLE IF EXISTS Tipologia")
            cursor.execute("DROP TABLE IF EXISTS Personas")
            cursor.execute("DROP TABLE IF EXISTS Causas")
            print("Tablas eliminadas (si existían)")
            
            create_causas = """
            CREATE TABLE Causas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Num_expediente VARCHAR(50),
                Nom_distrito VARCHAR(30),
                Nom_barrio VARCHAR(30),
                Nom_calle VARCHAR(50),
                Cod_postal VARCHAR(15),
                Descripcion_dia_semana VARCHAR(20),
                Descripcion_tipo_dia VARCHAR(20),
                Ano INTEGER,
                Mes_ano INTEGER,
                Nom_mes VARCHAR(10),
                Dia_mes VARCHAR(2),
                Hora_dia VARCHAR(2),
                Descripcion_turno VARCHAR(20),
                Descripcion_causa_mediata VARCHAR(50),
                Coordenada_X FLOAT,
                Coordenada_Y FLOAT,
                INDEX idx_num_expediente (Num_expediente)
            )
            """
            cursor.execute(create_causas)
            print("Tabla Causas creada exitosamente")
            
            create_personas = """
            CREATE TABLE Personas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Num_expediente VARCHAR(50),
                Descripcion_sexo VARCHAR(10),
                Descripcion_tipos_persona VARCHAR(20),
                Edad VARCHAR(10),
                Descripcion_victimizacion VARCHAR(20),
                INDEX idx_num_expediente (Num_expediente)
            )
            """
            cursor.execute(create_personas)
            print("Tabla Personas creada exitosamente")
            
            create_tipologia = """
            CREATE TABLE Tipologia (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Num_expediente VARCHAR(50),
                Descripcion_tipos_accidente VARCHAR(20),
                INDEX idx_num_expediente (Num_expediente)
            )
            """
            cursor.execute(create_tipologia)
            print("Tabla Tipologia creada exitosamente")
            
            create_vehiculos = """
            CREATE TABLE Vehiculos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Num_expediente VARCHAR(50),
                Descripcion_tipos_vehiculo VARCHAR(20),
                Descripcion_modelo VARCHAR(20),
                Descripcion_marca VARCHAR(20),
                Descripcion_color VARCHAR(20),
                Descripcion_carnet VARCHAR(20),
                Antiguedad_carnet INTEGER,
                INDEX idx_num_expediente (Num_expediente)
            )
            """
            cursor.execute(create_vehiculos)
            print("Tabla Vehiculos creada exitosamente")
            
            print("\n¡Todas las tablas han sido creadas exitosamente!")
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    create_database_and_tables()

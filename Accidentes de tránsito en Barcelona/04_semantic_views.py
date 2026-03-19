import mysql.connector
from mysql.connector import Error
import pandas as pd
import warnings
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy')

def create_semantic_view():
    """
    Script para crear y consultar una vista semántica de accidentes mortales
    """
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='AccidentesBCN'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("=" * 110)
            print("Creando vista semántica: vista_accidentes_mortales")
            print("=" * 110)
            
            cursor.execute("DROP VIEW IF EXISTS vista_accidentes_mortales")
            print("\nVista eliminada (si existía)")
            
            create_view = """
            CREATE VIEW vista_accidentes_mortales AS
            WITH accidentes AS (
            SELECT 
                CAST(Ano AS UNSIGNED) AS Ano,
                CAST(Mes_ano AS UNSIGNED) AS Mes_ano,
                CAST(Dia_mes AS UNSIGNED) AS Dia_mes,
                CAST(Hora_dia AS UNSIGNED) AS Hora_dia,
                CONCAT(LPAD(Dia_mes, 2, '0'),'-', LPAD(Mes_ano, 2, '0') ,'-', Ano) AS Fecha,
                LPAD(Hora_dia,2,0) AS Hora,
                Descripcion_dia_semana,
                Nom_barrio AS Barrio,
                Descripcion_sexo AS Sexo,
                Descripcion_tipos_persona AS Persona, 
                Edad,
                estado_persona(Descripcion_victimizacion) AS Estado,
                Descripcion_tipos_accidente 
            FROM causas 
            INNER JOIN personas ON causas.Num_expediente= personas.Num_expediente
            INNER JOIN tipologia ON causas.Num_expediente= tipologia.Num_expediente
            )
            SELECT 
                CONCAT(Fecha,' ',Hora,':00:00') AS `Fecha y hora`, 
                Descripcion_dia_semana AS `Día`, 
                CONCAT(UPPER(LEFT(Barrio, 1)), SUBSTRING(Barrio, 2)) AS Barrio,
                Persona, 
                CASE WHEN Sexo LIKE 'H%' THEN 'Hombre' ELSE 'Mujer' END AS Sexo, 
                CAST(Edad AS SIGNED) AS Edad,
                Descripcion_tipos_accidente AS `Tipo de accidente`
            FROM accidentes 
            WHERE Estado= 'Muerto'
            ORDER BY Ano, Mes_ano, Dia_mes, Hora_dia
            """
            
            cursor.execute(create_view)
            print("✓ Vista semántica creada exitosamente\n")
            
            print("=" * 110)
            print("Consultando vista: 30 accidentes mortales aleatorios")
            print("=" * 110)
            
            query = """
            SELECT * FROM vista_accidentes_mortales
            ORDER BY RAND()
            LIMIT 30
            """
            
            df = pd.read_sql(query, connection)
            
            print(f"\nTotal de registros obtenidos: {len(df)}\n")
            print(df.to_string(index=False))
            
            print("\n" + "=" * 110)
            print("Resumen de la vista por día de la semana")
            print("=" * 110)
            
            stats_query = """
            SELECT 
                Día,
                COUNT(*) AS `Total de fallecidos`,
                ROUND(AVG(Edad), 1) AS `Edad promedio`,
                MIN(Edad) AS `Edad mínima`,
                MAX(Edad) AS `Edad máxima`
            FROM vista_accidentes_mortales
            GROUP BY Día
            ORDER BY FIELD(Día, 'Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte', 'Diumenge')
            """
            
            df_stats = pd.read_sql(stats_query, connection)
            
            print(f"\n{df_stats.to_string(index=False)}\n")
            
            print("=" * 110)
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    create_semantic_view()

import mysql.connector
from mysql.connector import Error
import pandas as pd
import warnings
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy')

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

def run_analysis_queries():
    """
    Script para ejecutar queries de análisis sobre la base de datos AccidentesBCN
    """
    
    queries = [
        {
            'nombre': 'Query 1: Las 10 avenidas/ calles más peligrosas',
            'sql': """
                SELECT 
                    Nom_calle AS `Avenida/Calle`, 
                    COUNT(DISTINCT(Num_expediente)) AS `Número de incidentes`
                FROM causas 
                GROUP BY Nom_calle 
                HAVING Nom_calle IS NOT NULL
                ORDER BY `Número de incidentes` DESC 
                LIMIT 10;                
            """
        },
        {
            'nombre': 'Query 2:  Los 10 accidentes más comunes',
            'sql': """
                SELECT 
                   Descripcion_tipos_accidente AS `Tipo de accidente`, 
                   COUNT(DISTINCT(Num_expediente)) AS `Número de incidentes`
                FROM tipologia 
                GROUP BY `Tipo de accidente`
                HAVING `Tipo de accidente` IS NOT NULL
                ORDER BY `Número de incidentes` DESC 
                LIMIT 10;               
            """
        },
        {
            'nombre': 'Query 3: Los 10 accidentes con la mayor cantidad de personas involucradas',
            'sql': """
                    WITH accidentes_personas AS (
                    SELECT 
                        Num_expediente AS N_incidente,
                        COUNT(Num_expediente) AS total_personas
                    FROM personas 
                    GROUP BY  Num_expediente
                    ORDER BY total_personas DESC LIMIT 10
                    )
                    SELECT 
                       CONCAT(LPAD(Dia_mes, 2, '0'),'-', LPAD(Mes_ano, 2, '0') ,'-', Ano) AS Fecha,
                       CONCAT(LPAD(Hora_dia,2,'0'),':00:00') AS Hora,
                       Nom_calle AS `Avenida/Calle`,
                       total_personas AS `Personas involucradas`
                    FROM accidentes_personas 
                    LEFT JOIN causas ON causas.Num_expediente= accidentes_personas.N_incidente;                    
            """
        },
        {
            'nombre': 'Query 4: Los 10 días con mayor cantidad de accidentes',
            'sql': """
                SELECT 
                    CONCAT(LPAD(Dia_mes, 2, '0'),'-', LPAD(Mes_ano, 2, '0') ,'-', Ano) AS Fecha,
                    COUNT(DISTINCT (Num_expediente)) AS `Número de accidentes`
                FROM causas
                GROUP BY Fecha
                ORDER BY `Número de accidentes` DESC
                LIMIT 10;                  
            """
        },
        {
           'nombre': 'Query 5: Víctimas mortales y heridos por tipo de vehículo y franja horaria',
           'sql': """
                SELECT 
                    tipo_vehiculo(Descripcion_tipos_vehiculo) AS `Tipo de vehículo`,
                    CASE 
                        WHEN Hora_dia BETWEEN 0 AND 5   THEN 'Madrugada (0-5h)'
                        WHEN Hora_dia BETWEEN 6 AND 13  THEN 'Mañana (6-13h)'
                        WHEN Hora_dia BETWEEN 14 AND 20 THEN 'Tarde (14-20h)'
                        ELSE                                 'Noche (21-23h)'
                    END AS `Franja horaria`,
                    CAST(SUM(CASE WHEN estado_persona(Descripcion_victimizacion) = 'Muerto'  THEN 1 ELSE 0 END) AS SIGNED) AS Muertos,
                    CAST(SUM(CASE WHEN estado_persona(Descripcion_victimizacion) = 'Herido'  THEN 1 ELSE 0 END) AS SIGNED) AS Heridos,
                    CAST(SUM(CASE WHEN estado_persona(Descripcion_victimizacion) = 'Ileso'  THEN 1 ELSE 0 END) AS SIGNED) AS Ilesos,
                    CAST(SUM(CASE WHEN estado_persona(Descripcion_victimizacion) = 'Desconocido'  THEN 1 ELSE 0 END) AS SIGNED) AS Desconocido
                FROM Causas
                INNER JOIN Vehiculos ON Causas.Num_expediente = Vehiculos.Num_expediente
                INNER JOIN Personas  ON Causas.Num_expediente = Personas.Num_expediente
                GROUP BY `Tipo de vehículo`, `Franja horaria`
                ORDER BY `Tipo de vehículo`, 
                    FIELD(`Franja horaria`, 'Madrugada (0-5h)', 'Mañana (6-13h)', 'Tarde (14-20h)', 'Noche (21-23h)');
           """
        },
        {
            'nombre': 'Query 6: Total de víctimas por año, mes y condición de estado (agrupado por año)',
            'sql': """
                WITH total_victimas AS (
                SELECT 
                    Ano AS Año, 
                    Mes_ano AS Mes_Numero,
                    Nom_mes AS Mes,
                    estado_persona(Descripcion_victimizacion) AS Estado, 
                    COUNT(estado_persona(Descripcion_victimizacion)) AS Total
                FROM Causas 
                INNER JOIN Personas ON Causas.Num_expediente = Personas.Num_expediente
                GROUP BY Ano, Nom_mes,Estado )
                SELECT 
                    Año,
                    CAST(SUM(CASE WHEN Estado= 'Ileso' THEN Total ELSE 0 END) AS SIGNED) AS Ilesos,
                    CAST(SUM(CASE WHEN Estado= 'Herido' THEN Total ELSE 0 END) AS SIGNED) AS Heridos,
                    CAST(SUM(CASE WHEN Estado= 'Muerto' THEN Total ELSE 0 END) AS SIGNED) AS Muertos,  
                    CAST(SUM(CASE WHEN Estado= 'Desconocido' THEN Total ELSE 0 END) AS SIGNED) AS Desconocido
                FROM total_victimas
                GROUP BY Año;
            """
        },
        {
            'nombre': 'Query 7: Total de personas involucradas por año, mes y categoría de edad',
            'sql': """
                WITH total_victimas AS (
                SELECT 
                    Ano AS Año, 
                    Mes_ano AS Mes_Numero,
                    Nom_mes AS Mes,
                    categoria_edad(NULLIF( NULLIF(Edad,'Desconegut'),-1)) AS Categoria, 
                    COUNT(categoria_edad(NULLIF( NULLIF(Edad,'Desconegut'),-1))) AS Total
                FROM Causas 
                INNER JOIN Personas ON Causas.Num_expediente = Personas.Num_expediente
                GROUP BY Ano, Mes, Categoria)
                SELECT 
                    Año,
                    Mes,
                    CAST(SUM(CASE WHEN Categoria= 'Bebé' THEN Total ELSE 0 END) AS SIGNED) AS Bebés,
                    CAST(SUM(CASE WHEN Categoria= 'Niño' THEN Total ELSE 0 END) AS SIGNED) AS Niños,
                    CAST(SUM(CASE WHEN Categoria= 'Adolescente' THEN Total ELSE 0 END) AS SIGNED) AS Adolescentes,  
                    CAST(SUM(CASE WHEN Categoria= 'Adulto' THEN Total ELSE 0 END) AS SIGNED) AS Adultos,
                    CAST(SUM(CASE WHEN Categoria= 'Mayor' THEN Total ELSE 0 END) AS SIGNED) AS Mayores,
                    CAST(SUM(CASE WHEN Categoria= 'Anciano' THEN Total ELSE 0 END) AS SIGNED) AS Ancianos,
                    CAST(SUM(CASE WHEN Categoria= 'Desconocido' THEN Total ELSE 0 END) AS SIGNED) AS Desconocido
                FROM total_victimas
                GROUP BY Año, Mes_Numero;
            """
        },
        {
            'nombre': 'Query 8: Total de vehículos implicados por año y categoría',
            'sql': """
                WITH total_vehiculos AS (
                SELECT 
                    Ano AS Año, 
                    tipo_vehiculo(Descripcion_tipos_vehiculo) AS Categoria, 
                    COUNT(tipo_vehiculo(Descripcion_tipos_vehiculo)) AS Total
                FROM Causas 
                INNER JOIN Vehiculos ON Causas.Num_expediente = Vehiculos.Num_expediente
                GROUP BY Ano, Categoria)
                SELECT 
                    Año,
                    CAST(SUM(CASE WHEN Categoria= 'Ambulancia' THEN Total ELSE 0 END) AS SIGNED) AS Ambulancias,
                    CAST(SUM(CASE WHEN Categoria= 'Bicicleta' THEN Total ELSE 0 END) AS SIGNED) AS Bicicletas,  
                    CAST(SUM(CASE WHEN Categoria= 'Bus' THEN Total ELSE 0 END) AS SIGNED) AS Buses,
                    CAST(SUM(CASE WHEN Categoria= 'Camión' THEN Total ELSE 0 END) AS SIGNED) AS Camiones,
                    CAST(SUM(CASE WHEN Categoria= 'Camper' THEN Total ELSE 0 END) AS SIGNED) AS Campers,
                    CAST(SUM(CASE WHEN Categoria= 'Carro' THEN Total ELSE 0 END) AS SIGNED) AS Carros,
                    CAST(SUM(CASE WHEN Categoria= 'Coche' THEN Total ELSE 0 END) AS SIGNED) AS Coches,
                    CAST(SUM(CASE WHEN Categoria= 'Maquinaria' THEN Total ELSE 0 END) AS SIGNED) AS Maquinarias,
                    CAST(SUM(CASE WHEN Categoria= 'Motocicleta' THEN Total ELSE 0 END) AS SIGNED) AS Motocicletas,
                    CAST(SUM(CASE WHEN Categoria= 'Taxi' THEN Total ELSE 0 END) AS SIGNED) AS Taxis,
                    CAST(SUM(CASE WHEN Categoria= 'Tractor' THEN Total ELSE 0 END) AS SIGNED) AS Tractores,
                    CAST(SUM(CASE WHEN Categoria= 'Tren' THEN Total ELSE 0 END) AS SIGNED) AS Trenes,
                    CAST(SUM(CASE WHEN Categoria= 'Triciclo' THEN Total ELSE 0 END) AS SIGNED) AS Triciclos,
                    CAST(SUM(CASE WHEN Categoria= 'Otros' THEN Total ELSE 0 END) AS SIGNED) AS Otros
                FROM total_vehiculos
                GROUP BY Año;
            """
        }
    ]
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='AccidentesBCN'
        )
        
        if connection.is_connected():
            for idx, query in enumerate(queries, 1):
                print("=" * 140)
                print(query['nombre'])
                print("=" * 140)
                
                df = pd.read_sql(query['sql'], connection)
                
                print(f"\nTotal de registros obtenidos: {len(df)}\n")
                
                if idx == 1:
                    print(f"{'Avenida/Calle':<50} {'Número de incidentes':>20}")
                    print("-" * 72)
                    for _, row in df.iterrows():
                        print(f"{row['Avenida/Calle']:<50} {row['Número de incidentes']:>20}")
                elif idx == 2:
                    print(f"{'Tipo de accidente':<50} {'Número de incidentes':>20}")
                    print("-" * 72)
                    for _, row in df.iterrows():
                        print(f"{row['Tipo de accidente']:<50} {row['Número de incidentes']:>20}")
                elif idx == 3:
                    print(f"{'Fecha':<15} {'Hora':<12} {'Avenida/Calle':<50} {'Personas involucradas':>20}")
                    print("-" * 99)
                    for _, row in df.iterrows():
                        print(f"{row['Fecha']:<15} {row['Hora']:<12} {row['Avenida/Calle']:<50} {row['Personas involucradas']:>20}")
                elif idx == 5:
                    print(f"{'Tipo de vehículo':<18} {'Franja horaria':<22} {'Muertos':>10} {'Heridos':>10} {'Ilesos':>10} {'Desconocido':>10}")
                    print("-" * 86)
                    for _, row in df.iterrows():
                        print(f"{row['Tipo de vehículo']:<18} {row['Franja horaria']:<22} {row['Muertos']:>10} {row['Heridos']:>10} {row['Ilesos']:>10} {row['Desconocido']:>10}")
                else:
                    print(df.to_string(index=False))
                
            print("\n" + "=" * 140)
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    run_analysis_queries()

import mysql.connector
from mysql.connector import Error

def create_mysql_functions():
    """
    Script para crear funciones en MySQL:
    - categoria_edad: Categoriza edades en grupos
    - tipo_vehiculo: Clasifica tipos de vehículos
    """
    
    connection = None
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
            
            cursor.execute("DROP FUNCTION IF EXISTS categoria_edad")
            print("Función categoria_edad eliminada (si existía)")
            
            create_categoria_edad = """
            CREATE FUNCTION categoria_edad(edad INT)
            RETURNS VARCHAR(20)
            DETERMINISTIC
            BEGIN
                DECLARE categoria VARCHAR(20);
                
                IF edad IS NULL THEN
                    SET categoria = 'Desconocido';
                ELSEIF edad >= 0 AND edad <= 5 THEN
                    SET categoria = 'Bebé';
                ELSEIF edad >= 6 AND edad <= 12 THEN
                    SET categoria = 'Niño';
                ELSEIF edad >= 13 AND edad <= 17 THEN
                    SET categoria = 'Adolescente';
                ELSEIF edad >= 18 AND edad <= 35 THEN
                    SET categoria = 'Joven';
                ELSEIF edad >= 36 AND edad <= 60 THEN
                    SET categoria = 'Adulto';
                ELSEIF edad >= 61 AND edad <= 80 THEN
                    SET categoria = 'Mayor';
                ELSEIF edad >= 81 THEN
                    SET categoria = 'Anciano';
                ELSE
                    SET categoria = 'Desconocido';
                END IF;
                
                RETURN categoria;
            END
            """
            
            cursor.execute(create_categoria_edad)
            print("✓ Función categoria_edad creada exitosamente\n")
            
            cursor.execute("DROP FUNCTION IF EXISTS tipo_vehiculo")
            print("Función tipo_vehiculo eliminada (si existía)")
            
            create_tipo_vehiculo = """
            CREATE FUNCTION tipo_vehiculo(descr VARCHAR(50))
            RETURNS VARCHAR(20)
            DETERMINISTIC
            BEGIN
                IF descr IS NULL OR descr = 'Desconegut' OR descr = 'Sense Informar' THEN
                    RETURN 'Otros';
                ELSEIF descr LIKE '%Turisme%' OR descr LIKE '%Turismo%' OR descr LIKE '%Pick-up%' OR descr LIKE '%terreny%' OR descr LIKE '%terreno%' THEN
                    RETURN 'Coche';
                ELSEIF  descr LIKE '%Furgoneta%' OR descr LIKE '%Autocaravana%' THEN
                RETURN 'Camper';
                ELSEIF descr LIKE 'Taxi%' THEN
                    RETURN 'Taxi';
                ELSEIF descr LIKE '%Motocicleta%' OR descr LIKE '%Ciclomotor%' THEN
                    RETURN 'Motocicleta';
                ELSEIF descr LIKE '%Bicicleta%' THEN
                    RETURN 'Bicicleta';
                ELSEIF descr LIKE 'Autob%' OR descr LIKE 'Autocar%' OR descr LIKE 'Microb%' THEN
                    RETURN 'Bus';
                ELSEIF descr LIKE '%Tren%' OR descr LIKE '%ranv%' OR descr LIKE '%tramvia%' THEN
                    RETURN 'Tren';
                ELSEIF descr LIKE '%Tracto%' THEN
                    RETURN 'Tractor';
                ELSEIF descr LIKE '%Cami%' THEN
                    RETURN 'Camión';
                ELSEIF descr LIKE '%Maquin%' THEN
                    RETURN 'Maquinaria';
                ELSEIF descr LIKE '%mbul%' THEN
                    RETURN 'Ambulancia';
                ELSEIF descr LIKE '%ricicle%' OR descr LIKE '%uadriciclo%' THEN
                    RETURN 'Triciclo';
                ELSEIF descr LIKE 'Carro%' THEN
                    RETURN 'Carro';
                ELSE
                    RETURN 'Otros';
                END IF;
            END
            """
            
            cursor.execute(create_tipo_vehiculo)
            print("✓ Función tipo_vehiculo creada exitosamente\n")
            
            cursor.execute("DROP FUNCTION IF EXISTS estado_persona")
            print("Función estado_persona eliminada (si existía)")
            
            create_estado_persona = """
            CREATE FUNCTION estado_persona(descripcion VARCHAR(50))
            RETURNS VARCHAR(20)
            DETERMINISTIC
            BEGIN
                IF descripcion LIKE '%Ferit%' THEN
                    RETURN 'Herido';
                ELSEIF descripcion LIKE '%Mort%' THEN
                    RETURN 'Muerto';
                ELSEIF descripcion LIKE '%Il%' OR descripcion LIKE '%il%' THEN
                    RETURN 'Ileso';
                ELSE
                    RETURN 'Desconocido';
                END IF;
            END
            """
            
            cursor.execute(create_estado_persona)
            print("✓ Función estado_persona creada exitosamente\n")
            
            print("=" * 60)
            print("PRUEBAS DE LAS FUNCIONES")
            print("=" * 60)
            
            print("\n--- Prueba categoria_edad ---")
            test_ages = [3, 10, 15, 25, 45, 70, 85, None]
            for age in test_ages:
                if age is None:
                    cursor.execute("SELECT categoria_edad(NULL) as categoria")
                else:
                    cursor.execute(f"SELECT categoria_edad({age}) as categoria")
                result = cursor.fetchone()
                print(f"  Edad {age}: {result[0]}")
            
            print("\n--- Prueba tipo_vehiculo ---")
            cursor.execute("""
                SELECT DISTINCT Descripcion_tipos_vehiculo, tipo_vehiculo(Descripcion_tipos_vehiculo) as tipo
                FROM Vehiculos
                ORDER BY tipo, Descripcion_tipos_vehiculo
                LIMIT 35
            """)
            results = cursor.fetchall()
            print(f"  {'Descripción Original':<30} {'Tipo Clasificado':<15}")
            print(f"  {'-'*30} {'-'*15}")
            for row in results:
                desc = row[0] if row[0] else 'NULL'
                tipo = row[1]
                print(f"  {desc:<30} {tipo:<15}")
            
            print("\n--- Prueba estado_persona ---")
            cursor.execute("""
                SELECT DISTINCT Descripcion_victimizacion, estado_persona(Descripcion_victimizacion) as estado
                FROM Personas
                ORDER BY estado, Descripcion_victimizacion
            """)
            results = cursor.fetchall()
            print(f"  {'Descripción Victimización':<30} {'Estado':<15}")
            print(f"  {'-'*30} {'-'*15}")
            for row in results:
                desc = row[0] if row[0] else 'NULL'
                estado = row[1] if row[1] else 'NULL'
                print(f"  {desc:<30} {estado:<15}")
            
            print("\n" + "=" * 60)
            print("¡Funciones creadas y probadas exitosamente!")
            print("=" * 60)
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    create_mysql_functions()

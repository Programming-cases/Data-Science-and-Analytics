# 🚗💥 Proyecto Accidentes Barcelona

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Status](https://img.shields.io/badge/Status-Completado-success)

> 📊 Un sistema completo de análisis de datos de accidentes de tránsito en Barcelona, desde la carga de datos hasta visualizaciones y queries avanzadas.

---

## 📖 Índice

- [¿Qué es este proyecto?](#-qué-es-este-proyecto)
- [¿Qué hace?](#-qué-hace)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso del Proyecto](#-uso-del-proyecto)
- [Los 5 Scripts Explicados](#-los-5-scripts-explicados)
- [Queries de Análisis](#-queries-de-análisis)
- [Funciones MySQL Personalizadas](#-funciones-mysql-personalizadas)
- [Vistas Semánticas](#-vistas-semánticas)
- [Resultados Destacados](#-resultados-destacados)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 ¿Qué es este proyecto?

Este proyecto analiza **más de 150,000 accidentes de tránsito** ocurridos en Barcelona entre 2010 y 2025. Utilizamos Python, MySQL y análisis de datos para descubrir patrones, tendencias y responder preguntas como:

- 🛣️ ¿Cuáles son las calles más peligrosas?
- ⏰ ¿A qué hora ocurren más accidentes mortales?
- 🏍️ ¿Qué tipo de vehículos están más involucrados en accidentes graves?
- 📅 ¿Qué días del año son más peligrosos?

---

## ✨ ¿Qué hace?

El proyecto automatiza todo el pipeline de análisis de datos:

```
CSV Files → MySQL Database → Data Processing → Analysis → Insights
```

**Pipeline completo:**

1. 🗄️ **Crea la base de datos** con 4 tablas relacionadas
2. 📥 **Carga 150K+ registros** desde archivos CSV
3. 🔧 **Define funciones personalizadas** para categorización
4. 👁️ **Genera vistas semánticas** para consultas rápidas
5. 📊 **Ejecuta 8 queries de análisis** con resultados formateados

---

## 📁 Estructura del Proyecto

```
ProyectoSQL/
│
├── 📂 Archivos/                    # Archivos CSV con los datos
│   ├── causas.csv                  # Información de los accidentes
│   ├── personas.csv                # Víctimas involucradas
│   ├── tipologia.csv               # Tipos de accidentes
│   └── vehiculos.csv               # Vehículos implicados
│
├── 🐍 01_schema.py                 # Crea el esquema de la BD
├── 🐍 02_load_staging.py           # Carga los datos CSV
├── 🐍 03_functions.py              # Define funciones MySQL
├── 🐍 04_semantic_views.py         # Crea vistas semánticas
├── 🐍 05_analysis_queries.py       # Ejecuta queries de análisis
│
├── 🦇 run_all.bat                  # Script para ejecutar todo
└── 📖 README.md                    # Este archivo
```

---

## 🔧 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

### 1. **Python 3.12+**

```bash
python --version
```

### 2. **MySQL Server** (MariaDB también funciona)

```bash
mysql --version
```

### 3. **Librerías de Python**

```bash
pip install mysql-connector-python pandas
```

---

## 🚀 Instalación

### Paso 1: Clona la carpeta

```bash
git init
git remote add origin https://github.com/Programming-cases/Data-Science-and-Analytics.git
git config core.sparseCheckout true
git sparse-checkout set 'Accidentes de tránsito en Barcelona'
git pull origin master
```

### Paso 2: Verifica que tienes los archivos CSV

Asegúrate de que la carpeta `Archivos/` contiene:

- ✅ `causas.csv`
- ✅ `personas.csv`
- ✅ `tipologia.csv`
- ✅ `vehiculos.csv`

### Paso 3: Configura MySQL

1. Inicia el servidor MySQL
2. Verifica que puedes conectarte:
   ```bash
   mysql -u root -p
   ```

### Paso 4: Configura las credenciales de MySQL

Edita los archivos Python (`01_schema.py`, `02_load_staging.py`, etc.) y actualiza las credenciales de conexión:

```python
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tu_contraseña',  # ← Pon tu contraseña de MySQL aquí
    database='AccidentesBCN'
)
```

> ⚠️ **Importante:** No subas tus credenciales a GitHub. Considera usar variables de entorno para mayor seguridad.

---

## 🎮 Uso del Proyecto

### Opción 1: Ejecutar Todo Automáticamente (Recomendado)

Simplemente ejecuta el archivo batch:

**Desde el Explorador:**

```
Doble clic en run_all.bat
```

**Desde PowerShell:**

```powershell
.\run_all.bat
```

**Desde CMD:**

```cmd
run_all.bat
```

### Opción 2: Ejecutar Scripts Individualmente

Si prefieres ejecutar paso a paso:

```bash
# Paso 1: Crear esquema
python 01_schema.py

# Paso 2: Cargar datos (puede tardar 2-3 minutos)
python 02_load_staging.py

# Paso 3: Crear funciones
python 03_functions.py

# Paso 4: Crear vistas
python 04_semantic_views.py

# Paso 5: Ejecutar análisis
python 05_analysis_queries.py
```

---

## 🔍 Los 5 Scripts Explicados

### 📄 `01_schema.py` - Creación del Esquema

**¿Qué hace?**

- Crea la base de datos `AccidentesBCN`
- Define 4 tablas con sus relaciones:
  - `Causas` (tabla principal)
  - `Personas` (víctimas)
  - `Tipologia` (tipos de accidentes)
  - `Vehiculos` (vehículos involucrados)

**Tiempo de ejecución:** ~1 segundo

**Salida esperada:**

```
✓ Base de datos 'AccidentesBCN' creada
✓ Tabla 'Causas' creada
✓ Tabla 'Personas' creada
✓ Tabla 'Tipologia' creada
✓ Tabla 'Vehiculos' creada
```

---

### 📥 `02_load_staging.py` - Carga de Datos

**¿Qué hace?**

- Lee los 4 archivos CSV
- Limpia y transforma los datos
- Inserta más de 150,000 registros en lotes de 4,000
- Maneja conversión de tipos y valores nulos

**Tiempo de ejecución:** ~2-3 minutos

**Salida esperada:**

```
Cargando causas.csv...
  ✓ 38,000 registros insertados
Cargando personas.csv...
  ✓ 85,000 registros insertados
Cargando tipologia.csv...
  ✓ 38,000 registros insertados
Cargando vehiculos.csv...
  ✓ 72,000 registros insertados
```

**Características especiales:**

- ✅ Convierte tipos numpy a Python nativos
- ✅ Maneja formato decimal europeo (coma → punto)
- ✅ Reemplaza NaN con NULL
- ✅ Trunca tablas antes de insertar

---

### 🔧 `03_functions.py` - Funciones MySQL

**¿Qué hace?**

- Crea 3 funciones MySQL personalizadas para categorización:

#### 1. `categoria_edad(edad)`

Clasifica personas por rango de edad:

```sql
- Bebé (0-2 años)
- Niño (3-12 años)
- Adolescente (13-17 años)
- Adulto (18-39 años)
- Mayor (40-64 años)
- Anciano (65+ años)
```

#### 2. `tipo_vehiculo(descripcion)`

Clasifica vehículos en categorías:

```sql
- Coche, Motocicleta, Bicicleta
- Bus, Taxi, Camión, Camper
- Ambulancia, Tractor, Tren, etc.
```

#### 3. `estado_persona(descripcion)`

Clasifica el estado de las víctimas:

```sql
- Herido (Ferit)
- Muerto (Mort)
- Ileso (Il/il)
- Desconocido (otros)
```

**Tiempo de ejecución:** ~2 segundos

**Incluye casos de prueba** para verificar que las funciones funcionan correctamente.

---

### 👁️ `04_semantic_views.py` - Vistas Semánticas

**¿Qué hace?**

- Crea la vista `vista_accidentes_mortales`
- Muestra solo accidentes con víctimas mortales
- Formatea fechas y horas legibles
- Capitaliza nombres de barrios
- Convierte códigos de sexo a "Hombre"/"Mujer"

**Vista creada:**

```sql
vista_accidentes_mortales
  - Fecha y hora (DD-MM-YYYY HH:00:00)
  - Día de la semana
  - Barrio
  - Tipo de persona
  - Sexo
  - Edad
  - Tipo de accidente
```

**Estadísticas generadas:**

- Total de fallecidos: **453**
- Edad promedio: **48 años**
- Distribución por sexo:
  - Hombres: 355 (78.4%)
  - Mujeres: 98 (21.6%)

**Tiempo de ejecución:** ~3 segundos

---

### 📊 `05_analysis_queries.py` - Queries de Análisis

**¿Qué hace?**

- Ejecuta 8 queries avanzadas
- Formatea resultados para mejor legibilidad
- Usa las funciones personalizadas creadas anteriormente

**Tiempo de ejecución:** ~10-15 segundos

---

## 📈 Queries de Análisis

### Query 1: Las 10 Calles Más Peligrosas 🛣️

```
Avenida/Calle                                      Número de incidentes
------------------------------------------------------------------------
Corts Catalanes                                                    6438
Diagonal                                                           5439
Meridiana                                                          2417
Litoral (Llobregat)                                                2298
Aragó                                                              2007
```

**Insight:** Las grandes avenidas concentran el mayor número de accidentes.

---

### Query 2: Los 10 Tipos de Accidentes Más Comunes 💥

```
Tipo de accidente                                  Número de incidentes
------------------------------------------------------------------------
Abast                                                             29880
Col.lisió lateral                                                 18826
Atropellament                                                     17012
Col.lisió fronto-lat                                              15658
```

**Insight:** Los alcances (Abast) son el tipo más común de accidente.

---

### Query 3: Accidentes con Más Personas Involucradas 👥

```
Fecha           Hora         Avenida/Calle                      Personas involucradas
-------------------------------------------------------------------------------------
03-03-2025      14:00:00     Diagonal                                              46
15-06-2023      17:00:00     València                                              25
20-06-2019      09:00:00     Espanya                                               21
```

**Insight:** El accidente más grave involucró 46 personas en Diagonal.

---

### Query 4: Los 10 Días Más Peligrosos 📅

Muestra las fechas con mayor número de accidentes registrados.

---

### Query 5: Víctimas por Tipo de Vehículo y Franja Horaria ⏰🚗

```
Tipo de vehículo   Franja horaria           Muertos    Heridos
--------------------------------------------------------------
Coche              Madrugada (0-5h)              30       9218
Coche              Mañana (6-13h)                62      50312
Coche              Tarde (14-20h)                82      66701
Coche              Noche (21-23h)                20      14535
Motocicleta        Madrugada (0-5h)              41       5502
Motocicleta        Mañana (6-13h)               104      44794
```

**Insights clave:**

- 🚗 **Coches en la tarde**: el escenario más peligroso (82 muertos)
- 🏍️ **Motocicletas en la mañana**: 104 muertos (más letal por franja)
- 🌙 **Madrugada**: Motocicletas más letales que coches

---

### Query 6: Víctimas por Año y Estado 📊

Muestra la evolución anual de:

- Ilesos
- Heridos
- Muertos
- Desconocidos

---

### Query 7: Personas Involucradas por Edad 👶👴

Categoriza víctimas por grupos de edad:

- Bebés, Niños, Adolescentes
- Adultos, Mayores, Ancianos

---

### Query 8: Vehículos Implicados por Año 🚙🏍️🚲

Muestra la evolución de vehículos involucrados por categoría:

- Coches, Motocicletas, Bicicletas
- Buses, Taxis, Camiones, etc.

---

## 🛠️ Funciones MySQL Personalizadas

### `categoria_edad(edad)`

**Uso:**

```sql
SELECT categoria_edad(25) AS categoria;
-- Resultado: 'Adulto'
```

**Casos de uso:**

- Análisis demográfico de víctimas
- Segmentación por grupos de edad
- Estadísticas de riesgo por edad

---

### `tipo_vehiculo(descripcion)`

**Uso:**

```sql
SELECT tipo_vehiculo('Turisme') AS tipo;
-- Resultado: 'Coche'
```

**Casos de uso:**

- Clasificación de vehículos involucrados
- Análisis de peligrosidad por tipo
- Estadísticas de flota

---

### `estado_persona(descripcion)`

**Uso:**

```sql
SELECT estado_persona('Ferit lleu') AS estado;
-- Resultado: 'Herido'
```

**Casos de uso:**

- Clasificación de gravedad
- Estadísticas de mortalidad
- Análisis de víctimas

---

## 👁️ Vistas Semánticas

### `vista_accidentes_mortales`

**Descripción:**
Vista optimizada que muestra solo accidentes con víctimas mortales, con datos formateados y legibles.

**Uso:**

```sql
SELECT * FROM vista_accidentes_mortales
WHERE Barrio = 'El Raval'
ORDER BY `Fecha y hora` DESC
LIMIT 10;
```

**Características:**

- ✅ Fechas formateadas (DD-MM-YYYY HH:00:00)
- ✅ Nombres de barrios capitalizados
- ✅ Sexo en español (Hombre/Mujer)
- ✅ Solo víctimas mortales
- ✅ Ordenada cronológicamente

---

## 🎯 Resultados Destacados

### 📊 Estadísticas Generales

- **Total de accidentes:** ~38,000
- **Total de víctimas:** ~180,000
- **Víctimas mortales:** 453
- **Período analizado:** 2010-2025
- **Vehículos involucrados:** ~72,000

### 🏆 Top Insights

1. **Calle más peligrosa:** Corts Catalanes (6,438 accidentes)
2. **Tipo de accidente más común:** Alcance (29,880 casos)
3. **Franja horaria más peligrosa:** Tarde (14-20h)
4. **Vehículo más involucrado:** Coches (66,701 heridos en tarde)
5. **Día más peligroso:** Viernes (85 fallecidos)

### 📉 Tendencias

- **Mortalidad:** Disminución general desde 2010
- **Accidentes con bicicletas:** Aumento significativo
- **Edad promedio de fallecidos:** 48 años
- **Género:** 78% hombres, 22% mujeres en accidentes mortales

---

## 🐛 Troubleshooting

### Problema: "Can't connect to MySQL server"

**Solución:**

1. Verifica que MySQL esté corriendo:
   ```bash
   mysql -u root -p
   ```
2. Revisa las credenciales en los scripts Python

---

### Problema: "Unknown column in field list"

**Solución:**

- Ejecuta primero `01_schema.py` para crear las tablas
- Verifica que los archivos CSV tengan las columnas correctas

---

### Problema: "File not found: causas.csv"

**Solución:**

- Verifica que la carpeta `Archivos/` existe
- Asegúrate de que los 4 archivos CSV están presentes
- Revisa la ruta en `02_load_staging.py`

---

### Problema: El script `02_load_staging.py` es muy lento

**Solución:**

- Es normal, procesa 150K+ registros
- Tiempo esperado: 2-3 minutos
- Puedes aumentar `batch_size` a 5000 para acelerar

---

### Problema: "bat: The term 'bat' is not recognized"

**Solución:**
En PowerShell, usa:

```powershell
.\run_all.bat
```

En CMD, usa:

```cmd
run_all.bat
```

---

## 📝 Notas Adicionales

### Rendimiento

- **Carga de datos:** ~2-3 minutos
- **Creación de funciones:** ~2 segundos
- **Queries de análisis:** ~10-15 segundos
- **Total pipeline:** ~3-4 minutos

### Personalización

Puedes modificar:

- **Batch size** en `02_load_staging.py` (línea 67)
- **Credenciales MySQL** en todos los scripts (considera usar variables de entorno)
- **Queries** en `05_analysis_queries.py`
- **Categorías** en las funciones de `03_functions.py`

### Contribuir al Proyecto

¿Quieres mejorar el proyecto? ¡Las contribuciones son bienvenidas!

1. Haz un **fork** del repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

---

**Tecnologías utilizadas:**

- Python 3.12
- MySQL 8.0 
- Pandas 2.0
- mysql-connector-python

---

### ⭐ ¿Te gustó el proyecto?

Por favor dame una ⭐ en GitHub. ¡Gracias!

---

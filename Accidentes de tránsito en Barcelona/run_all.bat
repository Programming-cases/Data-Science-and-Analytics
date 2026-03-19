@echo off
REM Script para ejecutar todos los programas Python del proyecto AccidentesBCN en orden
REM Autor: Juan Pablo Delzo
REM Fecha: Marzo 2026

echo ============================================================================
echo Proyecto AccidentesBCN - Ejecucion completa del pipeline
echo ============================================================================
echo.

echo [1/5] Creando esquema de base de datos...
echo ----------------------------------------------------------------------------
python 01_schema.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al crear el esquema de la base de datos
    pause
    exit /b 1
)
echo.

echo [2/5] Cargando datos desde archivos CSV...
echo ----------------------------------------------------------------------------
python 02_load_staging.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al cargar los datos
    pause
    exit /b 1
)
echo.

echo [3/5] Creando funciones MySQL personalizadas...
echo ----------------------------------------------------------------------------
python 03_functions.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al crear las funciones MySQL
    pause
    exit /b 1
)
echo.

echo [4/5] Creando vistas semanticas...
echo ----------------------------------------------------------------------------
python 04_semantic_views.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al crear las vistas semanticas
    pause
    exit /b 1
)
echo.

echo [5/5] Ejecutando queries de analisis...
echo ----------------------------------------------------------------------------
python 05_analysis_queries.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al ejecutar las queries de analisis
    pause
    exit /b 1
)
echo.

echo ============================================================================
echo Pipeline completado exitosamente!
echo ============================================================================
echo.
pause

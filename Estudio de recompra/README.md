# Estudio de Recompra - Online Retail 

El proyecto analiza datos de ventas online para entender el comportamiento de los clientes y predecir quiénes volverán a comprar.

## Flow de trabajo

**`Analisis.ipynb`** - El notebook principal con todo el análisis:
- **Carga de datos**: Dataset de transacciones online (más de 1 millón de registros)
- **Limpieza**: Eliminamos duplicados, devoluciones, valores negativos y países sin información completa.
- **Exploración**: Distribuciones de precios/cantidades, ventas por país y evolución temporal.
- **Segmentación**: Agrupamos clientes por recencia, frecuencia y gasto (RFM).
- **Modelo predictivo**: Probé `Logistic Regression`, `XGBoost` y `LightGBM` para predecir la probabilidad de recompra.

## Estructura del repo

```
├── data/
│   ├── online_retail.pkl          # Dataset procesado (rápido de cargar)
│   └── online_retail_II.xlsx      # Fuente original
├── src/
│   ├── extraccion.py              # Helper para cargar datos
│   └── anejo.py                   # Funciones auxiliares
├── imagenes/                      # Gráficos exportados
└── Analisis.ipynb                 # Notebook principal
```

## Resultado destacado

Con XGBoost, el modelo alcanza ~80% ROC-AUC identificando clientes que recomprarán. Las variables más importantes son:
- Última compra (recencia)
- Número de compras previas (frecuencia) 
- Gasto total acumulado

---

*Proyecto de ML para análisis de comportamiento de clientes retail.*

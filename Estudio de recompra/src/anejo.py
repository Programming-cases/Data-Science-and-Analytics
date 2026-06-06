import pandas as pd

def informacion(df:pd.DataFrame):
    """
    Muestra información básica del DataFrame.
    Args:
        df (pd.DataFrame): DataFrame a analizar.
    """
    print(f"Contiene {df.shape[0]:,} instancias y {df.shape[1]} atributos")
    print("Por año:")
    # Build DataFrame with proper alignment
    inf = {'Tipo de variable': df.dtypes}
    
    anos = sorted(df.InvoiceDate.dt.year.unique())
    for ano in anos:
        df_year= df[df.InvoiceDate.dt.year == ano]
        print(ano,f": {len(df_year):,} instancias.")
        inf[f'NA {ano}'] = df_year.isnull().sum()
        inf[f'NA {ano} %'] = round(df_year.isnull().sum()*100/len(df_year),1)
    
    # Create DataFrame and transpose for better readability
    resumen = pd.DataFrame(inf)
    print("\n",resumen)
    
    
def agrupar_clientes(df:pd.DataFrame) -> pd.DataFrame:
    """
    Muestra información básica de los clientes.
    Args:
        df (pd.DataFrame): DataFrame a analizar.
    """
    # Agrupar por cliente
    clientes = df.groupby('Customer ID').agg(
                Revenue_Total=('Revenue','sum'),                                              # Facturación total
                Num_Compras=('Invoice','nunique'),                                            # Número de compras distintas
                Primera_Compra=('InvoiceDate', 'min'),                                        # Primera compra
                Ultima_Compra=('InvoiceDate','max'),                                          # Última compra
                País=('Country', lambda x: x.mode().iloc[0] if not x.mode().empty else None)  # País moda. La primera opción era cogiendo el primero ('first')
            )

    # Ticket medio
    clientes['Ticket_Medio'] = (clientes['Revenue_Total'] / clientes['Num_Compras']).round(2)
    return clientes

def escalador_minmax(l:list,n:float) -> float:
    """
    Transforma entre 0 y 1.
    
    Args:
        l (list): Lista de valores numéricos.
        n (float): Valor a transformar.
    
    Returns:
        float: Valor transformado a 9 cifras significativas.
    """
    x=(n-min(l)) / (max(l)-min(l))
    return round(x,8)   
    
def curva_roc(metodo:str, test_y:pd.Series, prob_recompra:pd.Series,color:str):
    """
    Genera y guarda la curva ROC para un modelo.
    
    Args:
        metodo (str): Nombre del método (por ejemplo, 'Regresión Logística').
        test_y (pd.Series): Valores reales de la variable objetivo.
        prob_recompra (pd.Series): Probabilidades predichas.
        color (str): Color de la curva.
    """
    import matplotlib.pyplot as plt
    plt.style.use('fivethirtyeight') 
    from sklearn.metrics import roc_curve, auc

    fpr, tpr, _ = roc_curve(test_y, prob_recompra)
    roc_auc_lr = auc(fpr, tpr)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, color=color, lw=2, label=f'{metodo} (AUC = {roc_auc_lr:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='Clasificador aleatorio')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.axis('scaled')
    plt.xlabel('Tasa de Falsos Positivos')
    plt.ylabel('Tasa de Verdaderos Positivos')
    plt.title(f'Curva ROC — {metodo}')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(f'imagenes/{metodo}_roc.png', dpi=300, bbox_inches='tight')
    plt.show()



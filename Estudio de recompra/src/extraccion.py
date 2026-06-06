# Se ejecuta una vez para crear el pickle
import pandas as pd
import os

def load_from_pickle():
    """Load df from pickle file (very fast)"""
    return pd.read_pickle('data/online_retail.pkl')

if __name__ == "__main__":
    os.chdir("../Estudio de recompra/data")
    DATA_PATH = "online_retail_II.xlsx"
    xl = pd.ExcelFile(DATA_PATH)
    df = pd.concat([pd.read_excel(DATA_PATH, sheet_name=s) for s in xl.sheet_names], ignore_index=True)
    df.to_pickle('online_retail.pkl')
    print(f"Saved {len(df):,} rows to online_retail.pkl")

    

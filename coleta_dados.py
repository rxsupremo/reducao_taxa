import pandas as pd

def carregar_dados(caminho):
    try:
        df = pd.read_csv(caminho)
        return df
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")
        return pd.DataFrame()

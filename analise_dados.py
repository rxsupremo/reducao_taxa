def calcular_media(df):
    return round(df["Taxa de Conversao"].mean(), 4)

def conversao_por_canal(df):
    return df.groupby("Canal")["Taxa de Conversao"].mean().round(4)

def conversao_por_periodo(df, coluna_periodo):
    return df.groupby(coluna_periodo)["Taxa de Conversao"].mean()

def detectar_outliers(df):
    q1 = df["Taxa de Conversao"].quantile(0.25)
    q3 = df["Taxa de Conversao"].quantile(0.75)
    iqr = q3 - q1
    outliers = df[
        (df["Taxa de Conversao"] < q1 - 1.5 * iqr) |
        (df["Taxa de Conversao"] > q3 + 1.5 * iqr)
    ]
    return outliers

import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.io as pio


def gerar_histograma(df):
    os.makedirs("static", exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.hist(df["Taxa de Conversao"], bins=10, color='blue', edgecolor='black')
    plt.title("Distribuição da Taxa de Conversão")
    plt.xlabel("Taxa de Conversão")
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/histograma.png")
    plt.close()


def gerar_barra_horizontal(df):
    os.makedirs("static", exist_ok=True)
    df_plot = df.groupby("Canal")["Taxa de Conversao"].mean().sort_values()
    plt.figure(figsize=(10, 6))
    df_plot.plot(kind="barh", color="skyblue", edgecolor="black")
    plt.title("Taxa de Conversão por Canal")
    plt.xlabel("Taxa de Conversão")
    plt.ylabel("Canal")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/barra_canal.png")
    plt.close()

def gerar_barra_interativa(df):
    fig = px.bar(
        df,
        x="Taxa de Conversao",
        y="Canal",
        orientation="h",
        title="Taxa de Conversão por Canal",
        text="Taxa de Conversao"
    )
    fig.update_layout(height=500, margin=dict(l=50, r=50, t=50, b=50))
    fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')

    # Retorna HTML do gráfico
    return pio.to_html(fig, full_html=False)

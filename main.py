from coleta_dados import carregar_dados
from limpeza_dados import limpar_dados
from analise_dados import (
    calcular_media,
    conversao_por_canal,
    detectar_outliers,
    conversao_por_periodo
)
from visualizacao import gerar_histograma, gerar_barra_horizontal

def main():
    # Carregar e limpar os dados
    df = carregar_dados("dados/conversao.csv")
    df_limpo = limpar_dados(df)

    # Verificar colunas disponíveis
    print("Colunas disponíveis:", df_limpo.columns.tolist())

    # Renomear colunas para compatibilidade com funções
    df_limpo = df_limpo.rename(columns={
        "taxa_conversao": "Taxa de Conversao",
        "canal": "Canal"
    })

    # Verificar se as colunas renomeadas existem
    if "Taxa de Conversao" not in df_limpo.columns or "Canal" not in df_limpo.columns:
        print("❌ Erro: Colunas obrigatórias não encontradas no arquivo.")
        return

    # Análise estatística
    media = calcular_media(df_limpo)
    print(f"📊 Média de conversão: {media:.2f}")

    # Geração de gráficos
    gerar_histograma(df_limpo)
    gerar_barra_horizontal(df_limpo)
    print("📈 Gráficos gerados e salvos na pasta 'static/'.")

    # Análises adicionais
    print("\n📊 Taxa média por canal:")
    print(conversao_por_canal(df_limpo))

    print("\n📆 Taxa por mês:")
    try:
        print(conversao_por_periodo(df_limpo, "Mes"))
    except KeyError:
        print("⚠️ Coluna 'Mes' não encontrada para análise por período.")

    # Detecção de outliers
    print("\n🚨 Outliers encontrados:")
    print(detectar_outliers(df_limpo))

if __name__ == "__main__":
    main()

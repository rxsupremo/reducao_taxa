from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
from analise_dados import calcular_media, conversao_por_canal
from visualizacao import gerar_histograma, gerar_barra_horizontal, gerar_barra_interativa

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar session

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if usuario == 'admin' and senha == 'admin':
            session['usuario'] = usuario
            return redirect(url_for('canal'))
        else:
            erro = 'Credenciais inválidas.'
    return render_template('login.html', erro=erro)

@app.route('/')
def index():
    df = pd.read_csv("dados/conversao.csv")
    df = df.rename(columns={"taxa_conversao": "Taxa de Conversao", "canal": "Canal"})
    df["data_conversao"] = pd.to_datetime(df["data_conversao"])
    df["mes"] = df["data_conversao"].dt.strftime("%Y-%m")
    gerar_histograma(df)
    media = calcular_media(df)
    return render_template("index.html", media=media)

@app.route('/por-canal', methods=['GET'])
def canal():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    df = pd.read_csv('dados/conversao.csv')
    df = df.rename(columns={"taxa_conversao": "Taxa de Conversao", "canal": "Canal"})
    df["data_conversao"] = pd.to_datetime(df["data_conversao"])
    df["mes"] = df["data_conversao"].dt.strftime("%Y-%m")

    canal_selecionado = request.args.get("canal")
    mes_selecionado = request.args.get("mes")
    min_taxa = request.args.get("min_taxa", type=float)
    max_taxa = request.args.get("max_taxa", type=float)

    if canal_selecionado:
        df = df[df["Canal"] == canal_selecionado]
    if mes_selecionado:
        df = df[df["mes"] == mes_selecionado]
    if min_taxa is not None:
        df = df[df["Taxa de Conversao"] >= min_taxa]
    if max_taxa is not None:
        df = df[df["Taxa de Conversao"] <= max_taxa]

    gerar_barra_horizontal(df)
    taxa_por_canal = conversao_por_canal(df).to_dict()
    grafico_html = gerar_barra_interativa(df)

    canais_disponiveis = sorted(df["Canal"].unique().tolist())
    meses_disponiveis = sorted(df["mes"].unique().tolist())

    return render_template(
        'canal.html',
        taxa_por_canal=taxa_por_canal,
        canais=canais_disponiveis,
        meses=meses_disponiveis,
        canal_selecionado=canal_selecionado,
        mes_selecionado=mes_selecionado,
        min_taxa=min_taxa,
        max_taxa=max_taxa,
        grafico_html=grafico_html
    )

@app.route('/exportar', methods=['GET'])
def exportar():
    df = pd.read_csv('dados/conversao.csv')
    df = df.rename(columns={"taxa_conversao": "Taxa de Conversao", "canal": "Canal"})
    df["data_conversao"] = pd.to_datetime(df["data_conversao"])
    df["mes"] = df["data_conversao"].dt.strftime("%Y-%m")

    canal = request.args.get("canal")
    mes = request.args.get("mes")
    min_taxa = request.args.get("min_taxa", type=float)
    max_taxa = request.args.get("max_taxa", type=float)

    if canal:
        df = df[df["Canal"] == canal]
    if mes:
        df = df[df["mes"] == mes]
    if min_taxa is not None:
        df = df[df["Taxa de Conversao"] >= min_taxa]
    if max_taxa is not None:
        df = df[df["Taxa de Conversao"] <= max_taxa]

    return df.to_csv(index=False), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="dados_filtrados.csv"'
    }

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
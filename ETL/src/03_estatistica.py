"""Fase 4: estatistica descritiva, hipoteses, respostas e graficos."""
import matplotlib

matplotlib.use("Agg")  # sem janela: permite execucao automatizada

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from config import (  # noqa: E402
    CSV_TRATADO,
    DIAS_SEMANA,
    GRAFICOS_DIR,
    RESULTADOS_DIR,
    banner,
)

COR_BASE = "#9db4c0"
COR_DESTAQUE = "#1f6f8b"


# ---------------------------------------------------------- formatacao
def brl(valor: float) -> str:
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",")
    return "R$ " + texto.replace("X", ".")


def pct(valor: float) -> str:
    return f"{valor * 100:.1f}".replace(".", ",") + "%"


def inteiro(valor: float) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def veredito(condicao: bool) -> str:
    return "Confirmada" if condicao else "Refutada"


# ------------------------------------------------------------- graficos
def _salvar(arquivo: str) -> str:
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / arquivo, dpi=130)
    plt.close()
    return f"graficos/{arquivo}"


def _barras(serie, titulo, xlabel, ylabel, arquivo, formato,
            horizontal=False) -> str:
    """Barras com o maior valor destacado e rotulos de dados."""
    if horizontal:
        serie = serie.sort_values(ascending=True)
    cores = [COR_DESTAQUE if v == serie.max() else COR_BASE
             for v in serie.values]
    _, ax = plt.subplots(figsize=(9, 5))
    if horizontal:
        barras = ax.barh(serie.index, serie.values, color=cores)
    else:
        barras = ax.bar(serie.index, serie.values, color=cores)
    ax.bar_label(barras, labels=[formato(v) for v in serie.values],
                 padding=3)
    ax.set_title(titulo, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.margins(x=0.12 if horizontal else 0.02, y=0.1)
    return _salvar(arquivo)


# ------------------------------------------------------------ perguntas
def q1_faturamento_filial(df) -> dict:
    fat = df.groupby("Filial")["valor_total"].sum().sort_values(
        ascending=False)
    top = fat.index[0]
    mais_vendas = df["Filial"].value_counts().idxmax()
    grafico = _barras(
        fat, "Faturamento total por filial", "Filial",
        "Faturamento (R$)", "q1_faturamento_filial.png", brl)
    return {
        "pergunta": "Qual filial apresentou o maior faturamento?",
        "hipotese": "A filial com mais vendas (transações) também é a "
                    "de maior faturamento.",
        "resposta": f"{top}, com {brl(fat.iloc[0])} "
                    f"({pct(fat.iloc[0] / fat.sum())} do total).",
        "evidencia": "; ".join(f"{f}: {brl(v)}" for f, v in fat.items()),
        "validacao": f"{veredito(top == mais_vendas)} — a filial com mais "
                     f"vendas é {mais_vendas}.",
        "grafico": grafico,
    }


def q2_qtd_vendas_filial(df) -> dict:
    qtd = df["Filial"].value_counts()
    dif = (qtd.max() - qtd.min()) / qtd.max()
    grafico = _barras(
        qtd, "Quantidade de vendas por filial", "Filial",
        "Número de vendas", "q2_qtd_vendas_filial.png", inteiro)
    return {
        "pergunta": "Qual filial realizou a maior quantidade de vendas?",
        "hipotese": "O volume de vendas é equilibrado entre as filiais "
                    "(diferença entre maior e menor inferior a 10%).",
        "resposta": f"{qtd.index[0]}, com {inteiro(qtd.iloc[0])} vendas.",
        "evidencia": "; ".join(f"{f}: {inteiro(v)}" for f, v in qtd.items()),
        "validacao": f"{veredito(dif < 0.10)} — diferença entre maior e "
                     f"menor de {pct(dif)}.",
        "grafico": grafico,
    }


def q3_faturamento_linha(df) -> dict:
    fat = df.groupby("linha_produto")["valor_total"].sum()
    fat = fat.sort_values(ascending=False)
    top = fat.index[0]
    top_itens = df.groupby("linha_produto")["Quantidade"].sum().idxmax()
    grafico = _barras(
        fat, "Faturamento por linha de produto", "Faturamento (R$)",
        "Linha de produto", "q3_faturamento_linha_produto.png", brl,
        horizontal=True)
    return {
        "pergunta": "Qual linha de produto apresentou o maior "
                    "faturamento?",
        "hipotese": "A linha líder em faturamento também é a líder em "
                    "unidades vendidas.",
        "resposta": f"{top}, com {brl(fat.iloc[0])}.",
        "evidencia": "; ".join(f"{k}: {brl(v)}" for k, v in fat.items()),
        "validacao": f"{veredito(top == top_itens)} — a líder em unidades "
                     f"é {top_itens}.",
        "grafico": grafico,
    }


def q4_avaliacao_linha(df) -> dict:
    aval = df.groupby("linha_produto")["Avaliação"].mean()
    aval = aval.sort_values(ascending=False)
    amplitude = aval.max() - aval.min()
    grafico = _barras(
        aval.round(2), "Avaliação média por linha de produto",
        "Avaliação média (0 a 10)", "Linha de produto",
        "q4_avaliacao_linha_produto.png", lambda v: f"{v:.2f}",
        horizontal=True)
    return {
        "pergunta": "Qual linha de produto recebeu a melhor avaliação "
                    "média?",
        "hipotese": "As avaliações médias são homogêneas entre as linhas "
                    "(amplitude inferior a 0,5 ponto).",
        "resposta": f"{aval.index[0]}, com média {aval.iloc[0]:.2f}.",
        "evidencia": "; ".join(f"{k}: {v:.2f}" for k, v in aval.items()),
        "validacao": f"{veredito(amplitude < 0.5)} — amplitude de "
                     f"{amplitude:.2f} ponto(s).",
        "grafico": grafico,
    }


def q5_forma_pagamento(df) -> dict:
    pag = df["forma_pagamento"].value_counts()
    share = pag / pag.sum()
    _, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        pag.values,
        labels=[f"{k} ({inteiro(v)})" for k, v in pag.items()],
        autopct=lambda p: pct(p / 100), startangle=90,
        colors=[COR_DESTAQUE, COR_BASE, "#d9e2e8"],
        explode=[0.05] + [0] * (len(pag) - 1))
    ax.set_title("Formas de pagamento", fontweight="bold")
    grafico = _salvar("q5_formas_pagamento.png")
    return {
        "pergunta": "Qual foi a forma de pagamento mais utilizada?",
        "hipotese": "Nenhuma forma de pagamento concentra mais da "
                    "metade das vendas.",
        "resposta": f"{pag.index[0]}, com {inteiro(pag.iloc[0])} vendas "
                    f"({pct(share.iloc[0])}).",
        "evidencia": "; ".join(f"{k}: {pct(s)}" for k, s in share.items()),
        "validacao": f"{veredito(share.max() <= 0.5)} — a líder detém "
                     f"{pct(share.max())}.",
        "grafico": grafico,
    }


def q6_valor_medio(df) -> dict:
    media = df["valor_total"].mean()
    mediana = df["valor_total"].median()
    _, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(df["valor_total"], bins=30, kde=True,
                 color=COR_BASE, ax=ax)
    ax.axvline(media, color="crimson", linestyle="--",
               label=f"Média: {brl(media)}")
    ax.axvline(mediana, color="black", linestyle=":",
               label=f"Mediana: {brl(mediana)}")
    ax.set_title("Distribuição do valor total das vendas",
                 fontweight="bold")
    ax.set_xlabel("Valor total (R$)")
    ax.set_ylabel("Frequência")
    ax.legend()
    grafico = _salvar("q6_valor_medio.png")
    return {
        "pergunta": "Qual foi o valor médio das vendas?",
        "hipotese": "A média é maior que a mediana (distribuição "
                    "assimétrica à direita).",
        "resposta": f"{brl(media)} por venda.",
        "evidencia": f"média {brl(media)}; mediana {brl(mediana)}; "
                     f"desvio padrão {brl(df['valor_total'].std())}.",
        "validacao": f"{veredito(media > mediana)} — média "
                     f"{'>' if media > mediana else '<='} mediana.",
        "grafico": grafico,
    }


def q7_maior_venda(df) -> dict:
    linha = df.loc[df["valor_total"].idxmax()]
    q1, q3 = df["valor_total"].quantile([0.25, 0.75])
    limite = q3 + 1.5 * (q3 - q1)
    e_outlier = linha["valor_total"] > limite
    _, ax = plt.subplots(figsize=(9, 4))
    sns.boxplot(x=df["valor_total"], color=COR_BASE, ax=ax)
    ax.scatter(linha["valor_total"], 0, color="crimson", zorder=5,
               label=f"Maior venda: {brl(linha['valor_total'])}")
    ax.set_title("Posição da maior venda na distribuição",
                 fontweight="bold")
    ax.set_xlabel("Valor total (R$)")
    ax.legend()
    grafico = _salvar("q7_maior_venda.png")
    return {
        "pergunta": "Qual foi a maior venda registrada?",
        "hipotese": "A maior venda é um outlier estatístico (acima de "
                    "Q3 + 1,5 × IQR).",
        "resposta": f"{brl(linha['valor_total'])} (venda "
                    f"{linha['id_venda']}, filial {linha['Filial']}, "
                    f"linha {linha['linha_produto']}).",
        "evidencia": f"limite superior de outliers: {brl(limite)}.",
        "validacao": f"{veredito(e_outlier)} — a maior venda "
                     f"{'excede' if e_outlier else 'não excede'} "
                     f"o limite.",
        "grafico": grafico,
    }


def q8_dia_semana(df) -> dict:
    vendas = df["dia_semana"].value_counts().reindex(DIAS_SEMANA,
                                                     fill_value=0)
    top = vendas.idxmax()
    fim_semana = vendas[["Sábado", "Domingo"]].sum() / vendas.sum()
    grafico = _barras(
        vendas, "Quantidade de vendas por dia da semana",
        "Dia da semana", "Número de vendas",
        "q8_vendas_dia_semana.png", inteiro)
    return {
        "pergunta": "Em qual dia da semana ocorreu a maior quantidade "
                    "de vendas?",
        "hipotese": "O fim de semana concentra mais vendas do que o "
                    "esperado (2/7 = 28,6% do total).",
        "resposta": f"{top}, com {inteiro(vendas[top])} vendas.",
        "evidencia": "; ".join(f"{d}: {inteiro(v)}"
                               for d, v in vendas.items()),
        "validacao": f"{veredito(fim_semana > 2 / 7)} — sábado e domingo "
                     f"somam {pct(fim_semana)} das vendas.",
        "grafico": grafico,
    }


# --------------------------------------------------------------- saidas
def salvar_estatisticas(df: pd.DataFrame) -> pd.DataFrame:
    colunas = ["preco_unitario", "Quantidade", "Imposto", "valor_total",
               "custo_mercadoria", "receita_bruta", "Avaliação"]
    desc = df[colunas].describe().T.round(2)
    desc["mediana"] = df[colunas].median().round(2)
    desc.to_csv(RESULTADOS_DIR / "estatisticas_descritivas.csv",
                encoding="utf-8")
    return desc


def salvar_respostas(respostas: list[dict]) -> None:
    linhas = ["# Respostas às perguntas de negócio", ""]
    for i, r in enumerate(respostas, start=1):
        linhas += [
            f"## {i}. {r['pergunta']}",
            "",
            f"**Hipótese:** {r['hipotese']}",
            "",
            f"**Resposta:** {r['resposta']}",
            "",
            f"**Evidência:** {r['evidencia']}",
            "",
            f"**Validação da hipótese:** {r['validacao']}",
            "",
            f"![{r['pergunta']}]({r['grafico']})",
            "",
        ]
    (RESULTADOS_DIR / "respostas_negocio.md").write_text(
        "\n".join(linhas), encoding="utf-8")


def executar() -> None:
    if not CSV_TRATADO.exists():
        raise FileNotFoundError(
            f"{CSV_TRATADO} nao existe. Execute antes 02_etl_vendas.py.")
    df = pd.read_csv(CSV_TRATADO, parse_dates=["data_venda"])
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    banner("Estatística descritiva (camada tratada)")
    print(salvar_estatisticas(df).to_string())

    respostas = [
        q1_faturamento_filial(df),
        q2_qtd_vendas_filial(df),
        q3_faturamento_linha(df),
        q4_avaliacao_linha(df),
        q5_forma_pagamento(df),
        q6_valor_medio(df),
        q7_maior_venda(df),
        q8_dia_semana(df),
    ]
    salvar_respostas(respostas)

    banner("Respostas às perguntas de negócio")
    for i, r in enumerate(respostas, start=1):
        print(f"[{i}] {r['pergunta']}\n    Resposta: {r['resposta']}\n"
              f"    Hipótese: {r['validacao']}\n")
    banner("Fase 4 concluida: resultados em resultados/")


if __name__ == "__main__":
    executar()


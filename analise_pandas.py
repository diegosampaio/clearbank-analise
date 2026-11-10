"""RO1 - Versão alternativa com pandas (leitura + groupby) e comparação com a solução nativa.

Uso:
    python analise_pandas.py          # lê transacoes.csv e compara com relatorio.json
"""
import json
import math

import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"


def carregar_pandas(caminho=ARQUIVO_CSV):
    """Lê o CSV com pd.read_csv e devolve (df_valido, total_lidas, total_invalidas)."""
    df = pd.read_csv(caminho, dtype=str)
    total = len(df)

    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    data_ok = df["data"].fillna("").str.match(r"^\d{4}-\d{2}-\d{2}$")
    df["data"] = pd.to_datetime(df["data"].where(data_ok), format="%Y-%m-%d", errors="coerce")
    df["cliente_id"] = df["cliente_id"].fillna("").str.strip()
    df["tipo"] = df["tipo"].fillna("").str.strip().str.lower()

    mascara = (
        df["id"].notna()
        & (df["id"] % 1 == 0)
        & (df["cliente_id"] != "")
        & df["data"].notna()
        & df["tipo"].isin(["credito", "debito"])
        & (df["valor"] > 0)
        & df["valor"].map(lambda v: math.isfinite(v) if pd.notna(v) else False)
    )
    df = df[mascara].drop_duplicates(subset="id", keep="first").copy()
    df["id"] = df["id"].astype(int)
    return df, total, total - len(df)


def agrupar_pandas(df):
    """Agrupa por mês (AAAA-MM) com groupby e calcula as métricas."""
    df = df.assign(mes=df["data"].dt.strftime("%Y-%m"))
    stats = df.groupby("mes")["valor"].agg(["count", "mean", "max", "min"])
    credito = df[df["tipo"] == "credito"].groupby("mes")["valor"].sum().rename("credito")
    debito = df[df["tipo"] == "debito"].groupby("mes")["valor"].sum().rename("debito")
    resumo = stats.join(credito).join(debito).fillna(0.0)
    resumo["saldo"] = resumo["credito"] - resumo["debito"]
    return resumo


def comparar(resumo_nativo, resumo_pandas):
    """Compara, mês a mês, os valores da solução nativa com os do pandas."""
    if set(resumo_nativo) != set(resumo_pandas.index):
        return False
    pares = {
        "quantidade": "count",
        "total_credito": "credito",
        "total_debito": "debito",
        "saldo": "saldo",
        "media": "mean",
        "maior_valor": "max",
        "menor_valor": "min",
    }
    for mes, metricas in resumo_nativo.items():
        for chave_nativa, coluna in pares.items():
            if not math.isclose(metricas[chave_nativa], float(resumo_pandas.loc[mes, coluna]), abs_tol=0.01):
                return False
    return True


if __name__ == "__main__":
    df_validas, lidas, invalidas = carregar_pandas()
    resumo = agrupar_pandas(df_validas)
    print(f"Total de linhas lidas: {lidas}")
    print(f"Linhas válidas: {len(df_validas)}")
    print(f"Linhas inválidas: {invalidas}\n")
    print(resumo.round(2).to_string())

    try:
        with open(ARQUIVO_JSON, encoding="utf-8") as f:
            nativo = json.load(f)["resumo_mensal"]
        print("\nResultados idênticos à solução nativa:", comparar(nativo, resumo))
    except FileNotFoundError:
        print(f"\n{ARQUIVO_JSON} não encontrado: execute o notebook antes para comparar.")

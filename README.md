# ClearBank — Análise Financeira com Python

Projeto do desafio final do módulo de Python (Pós em IA e Automação). O notebook lê o histórico de transações da fintech fictícia **ClearBank**, valida e limpa os dados, gera métricas mensais, sinaliza transações suspeitas e exporta o resultado.

## Como executar

1. Abra `desafio-final.ipynb` no **Google Colab** ou no **Jupyter Notebook** (Python 3.10+).
2. Garanta que `transacoes.csv` esteja na mesma pasta (se não estiver, o notebook cria um arquivo de teste).
3. Execute todas as células em ordem (*Runtime → Run all*).

Para os opcionais: `pip install pandas matplotlib` (já instalados no Colab). A versão pandas também roda isolada com `python analise_pandas.py`.

## O que o notebook gera

- **Resumo da limpeza** (linhas lidas, válidas e inválidas) no terminal.
- **Relatório mensal** formatado: quantidade, crédito, débito, saldo, média, maior e menor valor.
- **Transações suspeitas** (valor acima de R$ 10.000,00).
- **`relatorio.json`** com o resultado completo da análise.
- **RO1:** análise com pandas (`groupby`) comparada à solução nativa → resultados idênticos.
- **RO2:** `grafico.png` — barras empilhadas de crédito/débito por mês com o saldo em linha.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `desafio-final.ipynb` | Notebook com código e saídas salvas |
| `transacoes.csv` | Dados de teste (19 válidos, 10 inválidos, 2 suspeitos) |
| `relatorio.json` | Relatório gerado |
| `analise_pandas.py` | Versão alternativa com pandas |
| `grafico.png` | Gráfico gerado com matplotlib |

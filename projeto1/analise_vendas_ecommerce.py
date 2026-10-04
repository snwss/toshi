"""Projeto: Análise de vendas de um e-commerce.

Execute este arquivo em um ambiente com pandas, numpy, matplotlib e seaborn.
Ele gera uma base fictícia, realiza as análises solicitadas e salva um painel
com quatro gráficos em "relatorio_vendas.png".
"""

import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def gera_dados_ficticios(num_registros=500):
    """Gera um DataFrame com dados fictícios de vendas."""
    produtos = {
        "Laptop Gamer": {"categoria": "Eletrônicos", "preco": 7500.00},
        "Mouse Vertical": {"categoria": "Acessórios", "preco": 250.00},
        "Teclado Mecânico": {"categoria": "Acessórios", "preco": 550.00},
        "Monitor Ultrawide": {"categoria": "Eletrônicos", "preco": 2800.00},
        "Cadeira Gamer": {"categoria": "Móveis", "preco": 1200.00},
        "Headset 7.1": {"categoria": "Acessórios", "preco": 800.00},
        "Placa de Vídeo": {"categoria": "Hardware", "preco": 4500.00},
        "SSD 1TB": {"categoria": "Hardware", "preco": 600.00},
    }
    cidades_estados = {
        "São Paulo": "SP", "Rio de Janeiro": "RJ", "Belo Horizonte": "MG",
        "Porto Alegre": "RS", "Salvador": "BA", "Curitiba": "PR", "Fortaleza": "CE",
    }

    dados_vendas = []
    data_inicial = datetime(2026, 1, 1)

    for i in range(num_registros):
        produto_nome = random.choice(list(produtos))
        cidade = random.choice(list(cidades_estados))
        quantidade = np.random.randint(1, 8)
        preco_base = produtos[produto_nome]["preco"]
        desconto = np.random.uniform(0.90, 1.00) if produto_nome in ["Mouse Vertical", "Teclado Mecânico"] else 1
        preco_unitario = round(preco_base * desconto, 2)

        dados_vendas.append({
            "ID_Pedido": 1000 + i,
            "Data_Pedido": data_inicial + timedelta(days=i // 5, hours=random.randint(0, 23)),
            "Nome_Produto": produto_nome,
            "Categoria": produtos[produto_nome]["categoria"],
            "Preco_Unitario": preco_unitario,
            "Quantidade": quantidade,
            "ID_Cliente": np.random.randint(100, 150),
            "Cidade": cidade,
            "Estado": cidades_estados[cidade],
        })

    df = pd.DataFrame(dados_vendas)
    df["Faturamento"] = df["Preco_Unitario"] * df["Quantidade"]
    df["Mes"] = df["Data_Pedido"].dt.to_period("M").astype(str)
    return df


def main():
    random.seed(42)
    np.random.seed(42)
    sns.set_theme(style="whitegrid", palette="deep")

    df_vendas = gera_dados_ficticios(500)
    print("Base criada com sucesso:", df_vendas.shape)
    print(df_vendas.head())

    # 1. O que vender? Produtos com maior quantidade comercializada.
    produtos_vendidos = df_vendas.groupby("Nome_Produto")["Quantidade"].sum().sort_values(ascending=False)

    # 2. Onde focar? Categorias com maior faturamento.
    receita_categoria = df_vendas.groupby("Categoria")["Faturamento"].sum().sort_values(ascending=False)

    # 3. Quando agir? Faturamento mensal.
    receita_mensal = df_vendas.groupby("Mes")["Faturamento"].sum()

    # 4. Para onde expandir? Faturamento por cidade.
    receita_cidade = df_vendas.groupby("Cidade")["Faturamento"].sum().sort_values(ascending=False)

    print("\n--- PRINCIPAIS RESULTADOS ---")
    print(f"Produto mais vendido: {produtos_vendidos.index[0]} ({produtos_vendidos.iloc[0]} unidades)")
    print(f"Categoria de maior faturamento: {receita_categoria.index[0]} (R$ {receita_categoria.iloc[0]:,.2f})")
    print(f"Melhor mês: {receita_mensal.idxmax()} (R$ {receita_mensal.max():,.2f})")
    print(f"Cidade com maior faturamento: {receita_cidade.index[0]} (R$ {receita_cidade.iloc[0]:,.2f})")
    print(f"Faturamento total: R$ {df_vendas['Faturamento'].sum():,.2f}")

    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle("Relatório de Análise de Vendas - E-commerce", fontsize=18, fontweight="bold")

    sns.barplot(x=produtos_vendidos.values, y=produtos_vendidos.index, ax=axes[0, 0], color="#4C78A8")
    axes[0, 0].set_title("Produtos mais vendidos (quantidade)")
    axes[0, 0].set_xlabel("Unidades vendidas")
    axes[0, 0].set_ylabel("")

    sns.barplot(x=receita_categoria.index, y=receita_categoria.values, ax=axes[0, 1], color="#F58518")
    axes[0, 1].set_title("Faturamento por categoria")
    axes[0, 1].set_xlabel("")
    axes[0, 1].set_ylabel("Faturamento (R$)")
    axes[0, 1].tick_params(axis="x", rotation=20)

    sns.lineplot(x=receita_mensal.index, y=receita_mensal.values, marker="o", linewidth=3, ax=axes[1, 0], color="#54A24B")
    axes[1, 0].set_title("Evolução mensal do faturamento")
    axes[1, 0].set_xlabel("Mês")
    axes[1, 0].set_ylabel("Faturamento (R$)")

    sns.barplot(x=receita_cidade.values, y=receita_cidade.index, ax=axes[1, 1], color="#E45756")
    axes[1, 1].set_title("Faturamento por cidade")
    axes[1, 1].set_xlabel("Faturamento (R$)")
    axes[1, 1].set_ylabel("")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("relatorio_vendas.png", dpi=200, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()

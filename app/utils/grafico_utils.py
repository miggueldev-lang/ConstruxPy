from flask import flash 
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Config global para matplotlib
plt.rcParams['axes.unicode_minus'] = False

def gerar_base64(fig):
    """Converte um gráfico matplotlib para uma string base64."""
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode('utf-8')


def grafico_vendas_por_dia(vendas):
    """Gera gráfico de linha com total de vendas por dia."""
    df = pd.DataFrame([{
        'data': v.data.date(),
        'valor_total': v.valor_total
    } for v in vendas])

    df_grouped = df.groupby('data').sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_grouped['data'], df_grouped['valor_total'], marker='o')
    ax.set_title("Total de Vendas por Dia")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valor Total (R$)")
    ax.grid(True)
    fig.tight_layout()

    flash('Trocado Pelo: Grafico de Vendas por Dia', 'info')

    return gerar_base64(fig)


def grafico_vendas_por_produto(vendas):
    """Gera gráfico de barras com total vendido por produto."""
    df = pd.DataFrame([{
        'produto': v.produto.nome,
        'valor_total': v.valor_total
    } for v in vendas])

    df_grouped = df.groupby('produto').sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_grouped['produto'], df_grouped['valor_total'], color='green')
    ax.set_title("Vendas por Produto")
    ax.set_xlabel("Produto")
    ax.set_ylabel("Total Vendido (R$)")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    flash('Trocado Pelo: Grafico de Vendas por Produtos', 'info')
    
    return gerar_base64(fig)


def grafico_vendas_por_usuario(vendas):
    """Gera gráfico de barras com total comprado por usuário."""
    df = pd.DataFrame([{
        'usuario': v.comprador.nome,
        'valor_total': v.valor_total
    } for v in vendas])

    df_grouped = df.groupby('usuario').sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df_grouped['usuario'], df_grouped['valor_total'], color='orange')
    ax.set_title("Vendas por Usuário")
    ax.set_xlabel("Usuário")
    ax.set_ylabel("Total Comprado (R$)")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    flash('Trocado Pelo: Grafico de Vendas por Usuário', 'info')
    
    return gerar_base64(fig)


def grafico_vendas_por_categoria(vendas):
    """Gera gráfico de pizza com percentual de vendas por categoria de produto."""
    df = pd.DataFrame([{
        'categoria': v.produto.categoria or 'Indefinida',
        'valor_total': v.valor_total
    } for v in vendas])

    df_grouped = df.groupby('categoria').sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df_grouped['valor_total'], labels=df_grouped['categoria'], autopct='%1.1f%%', startangle=90)
    ax.set_title("Participação por Categoria de Produto")
    fig.tight_layout()

    flash('Trocado Pelo: Grafico de Vendas por Categoria', 'info')

    return gerar_base64(fig)

def grafico_vendas_por_trimestre(vendas):
    """Gera gráfico de barras com total vendido por trimestre (ex: 1º tri. 2024)."""
    df = pd.DataFrame([{
        'data': v.data,
        'valor_total': v.valor_total
    } for v in vendas])

    df['data'] = pd.to_datetime(df['data'])

    df['trimestre'] = df['data'].dt.quarter.astype(str) + "° tri. " + df['data'].dt.year.astype(str)

    df_grouped = df.groupby('trimestre')['valor_total'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_grouped['trimestre'], df_grouped['valor_total'], color='#00c2ff')
    ax.set_title("Vendas por Trimestre")
    ax.set_xlabel("Trimestre")
    ax.set_ylabel("Valor Total (R$)")
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()

    return gerar_base64(fig)

def grafico_atividade_carteira(extratos):
    """Gera gráfico de linha mostrando movimentação da carteira por dia."""
    if not extratos:
        return None

    df = pd.DataFrame([{
        'data': e.data.date() if hasattr(e.data, 'date') else e.data, 
        'valor': e.valor
    } for e in extratos])

    df_grouped = df.groupby('data').sum().reset_index()
    df_grouped = df_grouped.sort_values('data')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_grouped['data'], df_grouped['valor'].cumsum(), marker='o')
    ax.set_title("Atividade de Carteira (Saldo Acumulado)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Saldo (R$)")
    ax.grid(True)
    fig.tight_layout()

    return gerar_base64(fig)

def gerar_curva_abc(vendas):
    """Gera gr´´afico de barras com classificação ABC dos produtos com base no valor total vendido"""
    if not vendas:
        return None
    
    df = pd.DataFrame([{
        'produto':v.produto.nome,
        'valor': v.valor_total
    } for v in vendas])

    df_grouped = df.groupby('produto')['valor'].sum().sort_values(ascending=False).reset_index()
    df_grouped['percentual'] = df_grouped['valor'] / df_grouped['valor'].sum() * 100
    df_grouped['acumulado'] = df_grouped['percentual'].cumsum()

    def classificar(p):
        if p <= 80:
            return 'A'
        elif p <= 95:
            return 'B'
        else:
            return 'C'
    df_grouped['classe'] = df_grouped['acumulado'].apply(classificar)


    fig, ax = plt.subplots(figsize=(10, 6))
    cores = {'A': '#007bff', 'B': '#ffc107', 'C': '#dc3545'}
    for classe, grupo in df_grouped.groupby('classe'):
        ax.bar(grupo['produto'], grupo['valor'], label=f'Classe {classe}', color=cores[classe])

    ax.set_title("Curva ABC de Produtos")
    ax.set_xlabel("Produto")
    ax.set_ylabel("Total Vendido (R$)")
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    fig.tight_layout()

    return gerar_base64(fig)
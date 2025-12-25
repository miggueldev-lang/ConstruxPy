def gerar_resumo_vendas(vendas):
    from collections import Counter
    from statistics import mean

    if not vendas:
        return {
            'total_vendido': 0,
            'total_vendas': 0,
            'ticket_medio': 0,
            'produto_mais_vendido': 'Nenhum',
            'ultima_venda': 'Nenhuma'
        }

    total_vendido = sum(v.valor_total for v in vendas)
    total_vendas = len(vendas)
    ticket_medio = total_vendido / total_vendas

    produtos = [v.produto.nome for v in vendas]
    produto_mais_vendido = Counter(produtos).most_common(1)[0][0]

    ultima_venda = max(vendas, key=lambda v: v.data)

    return {
        'total_vendido': total_vendido,
        'total_vendas': total_vendas,
        'ticket_medio': ticket_medio,
        'produto_mais_vendido': produto_mais_vendido,
        'ultima_venda': ultima_venda.data.strftime('%d/%m/%Y %H:%M')
    }

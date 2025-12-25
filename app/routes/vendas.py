from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Usuario, Carteira, Extrato, Venda, Produto

from app.utils.auth_decorators import login_requerido, vendedor_requerido, admin_requerido, admin_or_vendedor_requerido

from app.utils.grafico_utils import (
    grafico_vendas_por_dia,
    grafico_vendas_por_produto,
    grafico_vendas_por_usuario,
    grafico_vendas_por_categoria,
    grafico_vendas_por_trimestre,
    grafico_atividade_carteira,
    gerar_curva_abc
)
from app.utils.resumo_utils import (gerar_resumo_vendas)

vendas_bp = Blueprint('vendas', __name__, template_folder="../templates")

@vendas_bp.route('/graficos')
@login_requerido
@admin_or_vendedor_requerido
def mostrar_graficos():
    tipo = request.args.get("tipo", "dia")
    vendas = Venda.query.all()

    if not vendas:
        flash("Sem vendas registradas ainda.", 'info')
        return redirect(url_for('main.home'))

    if tipo == 'produto':
        plot_url = grafico_vendas_por_produto(vendas)
    elif tipo == 'usuario':
        plot_url = grafico_vendas_por_usuario(vendas)
    elif tipo == 'categoria':
        plot_url = grafico_vendas_por_categoria(vendas)
    elif tipo == "dia":
        plot_url = grafico_vendas_por_dia(vendas)
    elif tipo == "trimestre":
        plot_url = grafico_vendas_por_trimestre(vendas)
    else:
        flash("Tipo de gráfico inválido.", 'warning')
        return redirect(url_for('vendas.mostrar_graficos', tipo="dia"))

    return render_template('vendas/graficos.html', plot_url=plot_url, tipo=tipo)

@vendas_bp.route('/resumo')
def resumo_vendas():
    vendas = Venda.query.all()
    resumo = gerar_resumo_vendas(vendas)
    return render_template('vendas/resumo.html', resumo=resumo)

@vendas_bp.route('/curva-abc')
@login_requerido
@admin_or_vendedor_requerido
def curva_abc():
    vendas = Venda.query.all()
    if not vendas:
        flash("Sem vendas para gerar a Curva ABC.", "info")
        return redirect(url_for("main.home"))
    
    plot_url = gerar_curva_abc(vendas)
    return render_template("vendas/curva_abc.html", plot_url=plot_url)

@vendas_bp.route('/atividade-carteira')
@login_requerido
@admin_or_vendedor_requerido
def atividade_carteira():
    extratos = Extrato.query.order_by(Extrato.data).all()
    
    if not extratos:
        flash("Sem movimentações na carteira para mostrar.", "info")
        # Passa resumo vazio para evitar erro no template
        resumo = {
            "total_entradas": 0,
            "total_saidas": 0,
            "saldo_atual": 0,
        }
        return render_template('vendas/atividade_carteira.html', plot_url=None, resumo=resumo)

    plot_url = grafico_atividade_carteira(extratos)
    
    total_entradas = sum(e.valor for e in extratos if e.valor > 0)
    total_saidas = sum(e.valor for e in extratos if e.valor < 0)
    saldo_atual = total_entradas + total_saidas
    
    resumo = {
        "total_entradas": total_entradas,
        "total_saidas": abs(total_saidas),
        "saldo_atual": saldo_atual,
    }
    
    return render_template('vendas/atividade_carteira.html', plot_url=plot_url, resumo=resumo)


@vendas_bp.route('/comprar', methods=['GET', 'POST'])
@login_requerido
def comprar():
    produtos = Produto.query.all()
    usuario_id = session.get("usuario_id")
    usuario = Usuario.query.get(usuario_id)

    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])

        produto = Produto.query.get_or_404(produto_id)
        total = produto.preco * quantidade

        if produto.quantidade_estoque < quantidade:
            flash("Estoque insuficiente.", "danger")
        elif usuario.carteira.saldo < total:
            flash("Saldo insuficiente na carteira.", "danger")
        else:
            # Criar venda
            venda = Venda(
                produto_id=produto.id,
                usuario_id=usuario.id,
                quantidade=quantidade,
                valor_total=total
            )
            db.session.add(venda)

            # Atualiza estoque
            produto.quantidade_estoque -= quantidade

            # Atualiza carteira
            usuario.carteira.saldo -= total
            extrato = Extrato(
                carteira_id=usuario.carteira.id,
                valor=-total,
                descricao=f"Compra de {produto.nome}"
            )
            db.session.add(extrato)

            db.session.commit()
            flash("Compra realizada com sucesso!", "success")
            return redirect(url_for("main.home"))

    return render_template("vendas/comprar.html", produtos=produtos, usuario=usuario)


@vendas_bp.route('/vender', methods=['GET', 'POST'])
@login_requerido
@vendedor_requerido
def vender():
    produtos = Produto.query.all()
    usuarios = Usuario.query.filter(Usuario.tipo == 'usuario').all()

    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        usuario_id = int(request.form['usuario_id'])
        quantidade = int(request.form['quantidade'])
        desconto = float(request.form.get('desconto', 5))

        produto = Produto.query.get_or_404(produto_id)
        comprador = Usuario.query.get_or_404(usuario_id)
        total = produto.preco * quantidade * (1 - desconto / 100)

        if produto.quantidade_estoque < quantidade:
            flash("Estoque insuficiente.", "danger")
        elif comprador.carteira.saldo < total:
            flash("O comprador não possui saldo suficiente.", "danger")
        else:
            # Criar venda
            venda = Venda(
                produto_id=produto.id,
                usuario_id=comprador.id,
                vendedor_id=session.get("usuario_id"),
                quantidade=quantidade,
                valor_total=total,
                desconto=desconto
            )
            db.session.add(venda)

            # Atualiza estoque
            produto.quantidade_estoque -= quantidade

            # Atualiza carteira do comprador
            comprador.carteira.saldo -= total
            extrato = Extrato(
                carteira_id=comprador.carteira.id,
                valor=-total,
                descricao=f"Venda de {produto.nome} (com desconto)"
            )
            db.session.add(extrato)

            db.session.commit()
            flash("Venda registrada com sucesso!", "success")
            return redirect(url_for("main.home"))

    return render_template("vendas/vender.html", produtos=produtos, usuarios=usuarios)
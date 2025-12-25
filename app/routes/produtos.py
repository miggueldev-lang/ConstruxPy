from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.produto import Produto
from app.forms.produto_form import ProdutoForm
from app.utils.auth_decorators import admin_requerido, login_requerido, vendedor_requerido

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
@login_requerido
def listar():
    busca = request.args.get("busca", "")
    categoria = request.args.get("categoria", "")

    query = Produto.query
    if busca:
        query = query.filter(Produto.nome.ilike(f"%{busca}%"))
    if categoria:
        query = query.filter_by(categoria=categoria)
    
    produtos = query.all()
    categorias = [c[0] for c in db.session.query(Produto.categoria).distinct() if c[0]]

    return render_template('produtos/listar.html', produtos = produtos, categorias=categorias)

@produtos_bp.route('/criar', methods = ["GET", "POST"])
@admin_requerido
def criar():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome = form.nome.data,
            descricao = form.descricao.data,
            preco = form.preco.data,
            quantidade_estoque = form.quantidade_estoque.data,
            categoria = form.categoria.data,
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto criado com sucesso!')
        return redirect(url_for('produtos.listar'))
    return render_template('produtos/criar_editar.html', form = form)

@produtos_bp.route('/editar/<int:id>', methods = ["GET","POST"])
@admin_requerido
def editar(id):
    produto = Produto.query.get_or_404(id)
    form = ProdutoForm(obj = produto)
    if form.validate_on_submit():
        form.populate_obj(produto)
        db.session.commit()
        flash("Produto atualizado com sucesso!")
        return redirect(url_for('produtos.listar'))
    return render_template('produtos/criar_editar.html', form = form)

@produtos_bp.route('/deletar/<int:id>', methods=['POST'])
@admin_requerido
def deletar(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!')
    return redirect(url_for('produtos.listar'))
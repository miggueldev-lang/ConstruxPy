from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models import Usuario, Venda, Carteira, Extrato
from app.utils.auth_decorators import admin_requerido

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@admin_requerido
def listar():
    busca = request.args.get("busca", "")
    tipo = request.args.get("tipo", "")

    query = Usuario.query
    if busca:
        query = query.filter(Usuario.nome.ilike(f"%{busca}%"))
    if tipo:
        query = query.filter_by(tipo=tipo)

    usuarios = query.all()
    
    return render_template('usuarios/listar.html', usuarios=usuarios)


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_requerido
def editar(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.nome == "ADM-MASTER":
        flash("Você não pode editar o ADM-MASTER.", "danger")
        return redirect(url_for('usuarios.listar'))

    if request.method == 'POST':
        novo_tipo = request.form.get('tipo')
        if novo_tipo in ['usuario', 'vendedor', 'admin']:
            usuario.tipo = novo_tipo
            db.session.commit()
            flash('Tipo de usuário atualizado com sucesso!', 'success')
        else:
            flash('Tipo de usuário inválido.', 'danger')
        return redirect(url_for('usuarios.listar'))

    return render_template('usuarios/editar.html', usuario=usuario)


@usuarios_bp.route('/deletar/<int:id>', methods=['POST'])
@admin_requerido
def deletar(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.nome == "ADM-MASTER":
        flash("Você não pode deletar o ADM-MASTER.", "danger")
        return redirect(url_for('usuarios.listar'))

    vendas = Venda.query.filter_by(usuario_id=usuario.id).all()
    for venda in vendas:
        db.session.delete(venda)

    carteira = Carteira.query.filter_by(usuario_id=usuario.id).first()
    if carteira:
        db.session.delete(carteira)    

    db.session.delete(usuario)

    db.session.commit()
    flash("Usuário deletado com sucesso!", "success")
    return redirect(url_for('usuarios.listar'))
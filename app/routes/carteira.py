from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models import Usuario, Extrato
from app import db
from app.utils.auth_decorators import login_requerido

carteira_bp = Blueprint('carteira', __name__, url_prefix='/carteira')

@carteira_bp.route("/detalhes")
def detalhes():
    usuario_id = session['usuario_id']
    usuario = Usuario.query.get(usuario_id)
    extratos = usuario.carteira.extratos[::-1]

    return render_template('carteira_detalhes.html', usuario=usuario, extratos=extratos)

@carteira_bp.route('/adicionar', methods=["POST"])
def adicionar_saldo():
    valor = float(request.form.get("valor", 0))
    if valor > 0:
        usuario = Usuario.query.get(session['usuario_id'])
        usuario.carteira.saldo += valor

        novo_extrato = Extrato(
            descricao=f"Depósito de R${valor}",
            valor = valor,
            carteira = usuario.carteira
        )
        db.session.add(novo_extrato)
        db.session.commit()
        flash("Saldo adicionado com sucesso!", "success")
    else:
        flash("Valor Inválido.", "danger")
    return redirect(url_for("carteira.detalhes"))
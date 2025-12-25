from flask import Blueprint, render_template, session
from app.utils.auth_decorators import login_requerido
from app.models import Usuario

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_requerido
def home():
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('home.html', usuario=usuario)

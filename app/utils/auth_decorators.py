from functools import wraps
from flask import redirect, session, url_for, flash

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa estar logado para acessar a essa página", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usuario_tipo") != "admin":
            flash("Acesso negado: apenas administradores podem acessar.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

def vendedor_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usuario_tipo") != "vendedor":
            flash("Acesso negado: apenas vendedores podem acessar.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

def admin_or_vendedor_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usuario_tipo") != "admin" and session.get("usuario_tipo") != "vendedor":
            flash("Acesso negado: apenas administradores ou vendedores podem acessar.", "danger")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function
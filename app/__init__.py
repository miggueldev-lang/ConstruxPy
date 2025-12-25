from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    csrf = CSRFProtect(app)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes.produtos import produtos_bp
    app.register_blueprint(produtos_bp)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    from app.routes.vendas import vendas_bp
    app.register_blueprint(vendas_bp)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp)
    from app.routes.carteira import carteira_bp
    app.register_blueprint(carteira_bp)

    return app
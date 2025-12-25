from app import db
from datetime import datetime

class Extrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255))
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    carteira_id = db.Column(db.Integer, db.ForeignKey('carteira.id'))

from app import db
from datetime import datetime

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    desconto = db.Column(db.Float, default=0.0)

    produto = db.relationship('Produto', backref='vendas')
    comprador = db.relationship('Usuario', foreign_keys=[usuario_id], backref='compras')
    vendedor = db.relationship('Usuario', foreign_keys=[vendedor_id], backref='vendas_feitas')
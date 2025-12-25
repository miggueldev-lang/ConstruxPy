from app import db

class Carteira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float, default=0.0)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True)
    usuario = db.relationship('Usuario', back_populates='carteira')

    extratos = db.relationship('Extrato', backref='carteira', lazy=True)
    
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    preco = FloatField('Preço', validators=[DataRequired()])
    quantidade_estoque = IntegerField('Quantidade em Estoque', validators=[DataRequired()])
    categoria = StringField('Categoria')
    submit = SubmitField('Salvar')

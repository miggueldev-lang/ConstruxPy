from app import create_app, db
from app.models import Usuario, Produto, Carteira

app = create_app()

def criar_banco():
    with app.app_context():
        db.create_all()
        print("✅ Banco de Dados criado com sucesso!")

def add_produtos():
    with app.app_context():
        produtos = [
            Produto(
                nome="Cimento CP II",
                descricao="Cimento para obras em geral (50kg)",
                preco=42.50,
                quantidade_estoque=100,
                categoria="Cimento"
            ),
            Produto(
                nome="Tijolo Baiano",
                descricao="Tijolo 39x19x14cm com 8 furos",
                preco=1.30,
                quantidade_estoque=2000,
                categoria="Alvenaria"
            ),
            Produto(
                nome="Areia Lavada (m³)",
                descricao="Areia para construção peneirada e limpa",
                preco=90.00,
                quantidade_estoque=50,
                categoria="Agregados"
            ),
            Produto(
                nome="Telha Colonial",
                descricao="Telha cerâmica para coberturas residenciais",
                preco=2.90,
                quantidade_estoque=800,
                categoria="Cobertura"
            )
        ]

        db.session.bulk_save_objects(produtos)
        db.session.commit()
        print("✅ Produtos inseridos com sucesso!")

def add_adm():
    with app.app_context():
        user_adm = Usuario(
            nome="ADM-MASTER",
            email="amdmaster@gmail.com",
            tipo="admin",
        )
        user_adm.set_senha("adm5549")
        db.session.add(user_adm)
        db.session.commit()
        print("✅ Usuario (ADM-MASTER) inserido com sucesso!")
    
criar_banco()
add_produtos()
add_adm()

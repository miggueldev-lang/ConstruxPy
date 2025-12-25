# 🏗️ConstruxPy
ConstruxPy é um sistema web desenvolvido em Python (Flask) com foco na simulação de construções, permitindo estimar custos de materiais, organizar dados financeiros e visualizar métricas por meio de gráficos.
O projeto evolui a partir de um sistema de gestão tradicional para uma proposta mais autoral: simular, planejar e analisar construções.

## 📖Visão Geral
O ConstruxPy nasceu como um sistema de controle e gestão, 
mas está sendo evoluído para um simulador de construção, onde será possível:
- Definir plantas de construções
- Trabalhar com escalas (ex: 1:50, 1:100)
- Estimar quantitativos de materiais
- Simular custos com base em preços reais
- Analisar dados financeiros por meio de graficos
A ideia central é unir engenharia básica, gestão e análise de dados em um único sistema.

## ⚙️Funcionalidades Atuais
Atulmente o projeto conta com:
- Cadastro e autenticação de usuários
- Sistema de produtos
- Registro de vendas
- Controle financeiro básico (carteira e extrato)
- Geração de gráficos a partir das vendas
- Organização a partir das vendas
- Organização modular seguindo boas praticas com Flask
- Banco de dados local utilizando SQLAlchemy (fase atual)

## 🚧Funcionalidades Planejadas (Roadmap)
AS próximas etapas do ConstruxPy incluem:
### 🏠Simulação de Construção
- Definição de uma planta de uma construção
- Escolha da escala da planta
- Associação da planta a um usuário
- Armazenamento da Planta como uma imagem

### 📐Calculo de Materiais
- Estimativa automática de materiais (cimento, areia, tijolos, etc.)
- Base de cálculo a partir da planta e escala
- Simulação de custo total da obra

### 💰Preços de Materiais
- Integração com API de preços de materiais de construção
- Suporte a múltiplas marcas e fornecedores
- Possível criação de API própria para padronização de preços

### 📊Análise de Dados
- Gráficos financeiros mais avançados
- Histórico de simulações
- Comparação entre diferentes construções
- Uso intensivo de Pandas e Matplotlib

### ☁️Infraestrutura
- Migração do banco de dados local para Supabase
- Persistência de usuários, vendas, extratos e plantas
- Preparação para deploy em ambiente produtivo

## 🛠️Tecnologias Utilizadas
### Backend
- Python
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Migrate
- WTForms
### Banco de dados
- SQLAlchemy (atualmente local)
- Supabase (planejado)
### Análise e visualização de Dados
- Pandas
- Matplotlib
### Outros
- Gunicorn
- python-dotenv
- email-validator

## 📂Estrutura do Projeto
```text
ConstruxPy/
│
├── app/
│   ├── forms/
│   ├── models/
│   │   ├── carteira.py
│   │   ├── extrato.py
│   │   ├── produto.py
│   │   ├── usuario.py
│   │   └── venda.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── carteira.py
│   │   ├── main.py
│   │   ├── produto.py
│   │   ├── usuario.py
│   │   └── venda.py
│   ├── static/
│   │   └── css/
│   │       ├── carteira.css
│   │       ├── graficos.css
│   │       ├── login.css
│   │       └── loja.css
│   ├── templates/
│   │   ├── produtos/
│   │   │   ├── criar_editar.html
│   │   │   └── listar.html
│   │   ├── usuarios/
│   │   │   ├── criar_editar.html
│   │   │   └── listar.html
│   │   ├── vendas/
│   │   │   ├── atividade_carteira.html
│   │   │   ├── base_vendas.html
│   │   │   ├── comprar.html
│   │   │   ├── curva_abc.html
│   │   │   ├── graficos.html
│   │   │   ├── resumo.html
│   │   │   └── vender.css
│   │   ├── base.html
│   │   ├── cadastro.html
│   │   ├── carteira_detalhes.html
│   │   ├── home.html
│   │   └── login.html
│   ├── utils/
│   │   ├── auth_decorators.py
│   │   ├── grafico_utils.py
│   │   └── resumo_utils.py
│   ├── __init__.py
│   └── config.py
│
├── instance/
│   └── db.sqlite3
│
├── requirements.txt
├── main.py
├── teste.py
└── README.md
└── .gitignore
```

## 🚀Como Executar o Projeto
### Pré-requisitos
- Python 3.10+
- Git
### Passos
```bash
git clone https://github.com/miggueldev-lang/ConstruxPy.git
cd ConstruxPy
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
### acesse no navegador
```arduino
http://localhost:5000
```

## 🧪Script de Testes
O arquivo teste.py contém scripts auxiliares para:
- Criação de usuário administrador com senha e email padrão
- Inserção de dados de teste no banco
- Facilitar desennvolvimento local

## 📌Status do Projeto
### 🚧Em desenvolvimento ativo
### 🔄 Em processo de refatoração para nova proposta de simulação de construção

## 👤 Autor
### Desenvolvido por João Miguel 
Todo o projeto — desde a concepção da ideia, arquitetura, implementação e evolução — é de autoria do desenvolvedor.

## 📄Licença
- ### [MIT](https://github.com/miggueldev-lang/ConstruxPy/blob/main/LICENSE)

## 🔚Considerações Finais
O ConstruxPy não é apenas um sistema CRUD, mas um projeto em evolução que busca unir programação, engenharia básica e análise de dados, servindo tanto como ferramenta prática quanto como projeto de portfólio avançado.

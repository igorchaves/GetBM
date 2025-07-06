from app import db

class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True, index=True)
    codigo = db.Column('codigo_categoria', db.String(20), unique=True, nullable=False)
    nome = db.Column('nome_categoria', db.String(100), nullable=False)


from app import db

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True, index=True)
    codigo = db.Column('codigo_status', db.String, unique=True, nullable=False)
    nome = db.Column('nome_status', db.String, nullable=False)

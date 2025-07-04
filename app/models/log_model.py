from datetime import datetime
from app import db

class LogAuditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tabela = db.Column(db.String(50), nullable=False)
    acao = db.Column(db.String(20), nullable=False)
    id_registro = db.Column(db.Integer, nullable=False)
    dados_anteriores = db.Column(db.Text, nullable=True)
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)

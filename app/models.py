from datetime import date, timedelta, datetime
from app import db

# ----------------------------
# Modelo Sprint (já existente)
# ----------------------------
class Sprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def __init__(self, nome, data_inicio, duracao):
        self.nome = nome
        self.data_inicio = data_inicio
        self.duracao = duracao
        self.data_fim = self.calcular_data_fim()
        self.ativo = True

    def calcular_data_fim(self):
        dias_uteis = self.duracao * 5
        data = self.data_inicio
        while dias_uteis > 0:
            data += timedelta(days=1)
            if data.weekday() < 5:
                dias_uteis -= 1
        return data

# ----------------------------
# Modelo Usuario
# ----------------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_usuario = db.Column(db.String(10), unique=True, nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Usuario {self.codigo_usuario} - {self.nome_usuario}>"

# ----------------------------
# Modelo Log de Auditoria
# ----------------------------
class LogAuditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tabela = db.Column(db.String(50), nullable=False)         # Ex: 'usuario', 'sprint'
    acao = db.Column(db.String(20), nullable=False)           # Ex: 'exclusao', 'atualizacao'
    id_registro = db.Column(db.Integer, nullable=False)       # ID do registro afetado
    dados_anteriores = db.Column(db.Text, nullable=True)      # JSON com os dados antes da exclusão
    data_acao = db.Column(db.DateTime, default=datetime.utcnow)

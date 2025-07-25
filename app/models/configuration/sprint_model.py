from datetime import timedelta
from app import db

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
            if data.weekday() < 5:  # Segunda a sexta
                dias_uteis -= 1
            if dias_uteis > 0:
                data += timedelta(days=1)
        return data

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d'),
            'data_fim': self.data_fim.strftime('%Y-%m-%d'),
            'duracao': self.duracao
        }

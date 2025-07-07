from app import db

class Backlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id', ondelete='CASCADE'), nullable=False)
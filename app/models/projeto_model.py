from app import db

class Projeto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_projeto = db.Column(db.String(20), unique=True, nullable=False)
    nome_projeto = db.Column(db.String(100), nullable=False)
    vertical = db.Column(db.String(50), nullable=False)

    backlogs = db.relationship('Backlog', backref='projeto', cascade="all, delete-orphan")
    seguimentos = db.relationship('Seguimento', backref='projeto', cascade="all, delete-orphan")

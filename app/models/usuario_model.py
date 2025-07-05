from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_usuario = db.Column(db.String(10), unique=True, nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    projetos = db.relationship('Projeto', secondary='usuario_projeto', backref='usuarios')    

    def __repr__(self):
        return f"<Usuario {self.codigo_usuario} - {self.nome_usuario}>"
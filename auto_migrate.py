import os
from flask import Flask
from flask_migrate import upgrade, init, migrate, stamp
from app import create_app, db

app = create_app()

with app.app_context():
    # Garante que o diretório de migrações esteja inicializado
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_dir):
        init()

    # Marca o banco como atualizado com o modelo atual, se necessário
    stamp()

    # Gera uma nova migração com mensagem padrão
    migrate(message="Auto migration")

    # Aplica a migração ao banco de dados
    upgrade()

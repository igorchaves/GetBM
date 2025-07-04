import os
from flask import Flask
from flask_migrate import upgrade, init, migrate, stamp
from app import create_app, db
import app.models  # ✅ Garante que os modelos sejam carregados

app = create_app()

with app.app_context():
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_dir):
        init()

    stamp()
    migrate(message="Auto migration")
    upgrade()

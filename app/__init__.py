import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# ✅ Carrega as variáveis do .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

     # ✅ keY para autenticação e sessões
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # ✅ Usa apenas PostgreSQL (sem fallback para SQLite)
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL não está definida no .env")

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Importa e registra blueprints
    from app.routes import app as app_blueprint
    app.register_blueprint(app_blueprint)

    # ✅ Ativa o log global de operações no banco
    from app import log_db  # ativa os listeners do SQLAlchemy

    # ✅ Aplica migrações automaticamente se ativado
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        from flask_migrate import upgrade as migrate_upgrade
        with app.app_context():
            migrate_upgrade()

    return app

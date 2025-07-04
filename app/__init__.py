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

    # ✅ Chave para autenticação e sessões
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # ✅ Configuração do banco de dados
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL não está definida no .env")

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Importa os modelos para garantir que o SQLAlchemy os reconheça
    from app.models import Sprint, Usuario, Projeto, Backlog, Seguimento, LogAuditoria

    # ✅ Importa e registra todos os blueprints da pasta routes
    from app.routes import (
        index_bp,
        backlog_bp,
        categoria_bp,
        funcionalidades_bp,
        organograma_bp,
        projeto_bp,
        sprint_bp,
        status_bp,
        usuario_bp
    )

    app.register_blueprint(index_bp)
    app.register_blueprint(backlog_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(funcionalidades_bp)
    app.register_blueprint(organograma_bp)
    app.register_blueprint(projeto_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(usuario_bp)

    # ✅ Ativa o log global de operações no banco
    from app import log_db  # ativa os listeners do SQLAlchemy

    # ✅ Aplica migrações automaticamente se ativado
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        from flask_migrate import upgrade as migrate_upgrade
        with app.app_context():
            migrate_upgrade()

    return app

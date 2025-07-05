import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Carrega o .env com base no FLASK_ENV
    env = os.getenv("FLASK_ENV", "development")
    dotenv_file = f".env.{env}"
    load_dotenv(dotenv_file)

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    # ✅ Chave para autenticação e sessões
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'chave-padrao-segura'

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
    from app.models import Sprint, Usuario, Projeto, Backlog, Seguimento, LogAuditoria, UsuarioProjeto

    # ✅ Importa todos os blueprints
    from app.routes.index_routes import index_bp
    from app.routes.backlog_routes import backlog_bp
    from app.routes.categoria_routes import categoria_bp
    from app.routes.funcionalidades_routes import funcionalidades_bp
    from app.routes.organograma_routes import organograma_bp
    from app.routes.projeto_routes import projeto_bp
    from app.routes.sprint_routes import sprint_bp
    from app.routes.status_routes import status_bp
    from app.routes.usuario_routes import usuario_bp

    # ✅ Registra todos os blueprints em bloco
    blueprints = [
        index_bp, backlog_bp, categoria_bp, funcionalidades_bp,
        organograma_bp, projeto_bp, sprint_bp, status_bp, usuario_bp
    ]

    for bp in blueprints:
        app.register_blueprint(bp)

    # ✅ Ativa o log global de operações no banco
    from app import log_db  # ativa os listeners do SQLAlchemy

    # ✅ Aplica migrações automaticamente se ativado
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        from flask_migrate import upgrade as migrate_upgrade
        with app.app_context():
            migrate_upgrade()

    return app
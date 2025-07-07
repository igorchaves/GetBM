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

   # 🔧 Inicialização de extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # 📦 Importação de modelos (necessária para o SQLAlchemy)
    from app import models 

    # 🌐 Registro de rotas
    from app.routes import register_routes
    register_routes(app)

    # 📝 Ativação de logs
    from app import log_db

    # 🔄 Migrações automáticas
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        from flask_migrate import upgrade as migrate_upgrade
        with app.app_context():
            migrate_upgrade()

    return app
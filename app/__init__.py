import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv  # ✅ Carrega variáveis do .env

# ✅ Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Cria a aplicação com os diretórios corretos
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///getbm.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa e registra o blueprint
    from app.routes import app as app_blueprint
    app.register_blueprint(app_blueprint)

    # ✅ Aplica migrações automaticamente se a variável estiver ativada
    if os.getenv("AUTO_MIGRATE", "false").lower() == "true":
        from flask_migrate import upgrade as migrate_upgrade
        with app.app_context():
            migrate_upgrade()

    return app

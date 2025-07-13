from app.routes.admin import usuario_bp, projeto_bp
from app.routes.configuration import status_bp, categoria_bp, funcionalidades_bp, sprint_bp, api_sprint_bp
from app.routes.home import home_bp
from app.routes.management import backlog_bp, organograma_bp
from app.routes.auth import auth_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(backlog_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(funcionalidades_bp)
    app.register_blueprint(organograma_bp)
    app.register_blueprint(projeto_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(api_sprint_bp)
 

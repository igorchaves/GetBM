from .index_routes import index_bp
from .backlog_routes import backlog_bp
from .categoria_routes import categoria_bp
from .funcionalidades_routes import funcionalidades_bp
from .organograma_routes import organograma_bp
from .projeto_routes import projeto_bp
from .sprint_routes import sprint_bp
from .status_routes import status_bp
from .usuario_routes import usuario_bp

def register_routes(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(backlog_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(funcionalidades_bp)
    app.register_blueprint(organograma_bp)
    app.register_blueprint(projeto_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(usuario_bp)

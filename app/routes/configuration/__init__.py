from .status_routes import status_bp
from .sprint_routes import sprint_bp
from .api_sprint import api_sprint_bp
from .funcionalidades_routes import funcionalidades_bp
from .categoria_routes import categoria_bp

__all__ = [
    'status_bp',
    'sprint_bp',
    'api_sprint_bp',
    'funcionalidades_bp',
    'categoria_bp'
]

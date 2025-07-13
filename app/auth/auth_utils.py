from flask import request, g
from functools import wraps
from app.auth.token_service import validar_token
from app.models.admin.usuario_model import Usuario

def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Primeiro tenta obter o token do cookie
        token = request.cookies.get('token')

        # Se não estiver no cookie, tenta no cabeçalho Authorization
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return {'erro': 'Token ausente'}, 401

        payload = validar_token(token)
        if not payload:
            return {'erro': 'Token inválido ou expirado'}, 401

        g.usuario_id = payload['usuario_id']
        request.is_superuser = payload.get('is_superuser', False)

        return f(*args, **kwargs)
    return wrapper


















def obter_usuario_logado():
    """
    Retorna o usuário logado com base no ID armazenado em g.usuario_id.
    Retorna None se for superusuário (ID 0) ou se o usuário não for encontrado.
    """
    if g.usuario_id == 0:
        return None  # Superusuário não está no banco

    return Usuario.query.get(g.usuario_id)
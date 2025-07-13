import jwt
from datetime import datetime, timezone, timedelta
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'chave-padrao-insegura')

def gerar_token(usuario_id, is_superuser=False):
    payload = {
        'usuario_id': usuario_id,
        'is_superuser': is_superuser,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload  # Retorna o dicionário completo
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


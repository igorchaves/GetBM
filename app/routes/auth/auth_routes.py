from flask import Blueprint, request, jsonify, render_template, make_response
from werkzeug.security import check_password_hash
from app.models.admin.usuario_model import Usuario
from app.auth.token_service import gerar_token
from app.auth.auth_utils import login_requerido, obter_usuario_logado
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota GET para exibir a tela de login
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

# Rota POST para autenticação
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    codigo = dados.get('usuario')
    senha = dados.get('senha')

    # ✅ Verificação de superusuário via .env
    superuser_codigo = os.getenv('SUPERUSER_CODIGO')
    superuser_senha = os.getenv('SUPERUSER_SENHA')

    if codigo == superuser_codigo and senha == superuser_senha:
        token = gerar_token(usuario_id=0)  # ID fictício para superusuário
        resp = make_response(jsonify({"mensagem": "Login bem-sucedido"}))
        resp.set_cookie('token', token, httponly=True, samesite='Lax')
        return resp

    # ✅ Verificação normal via banco de dados
    usuario = Usuario.query.filter_by(codigo_usuario=codigo).first()
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    token = gerar_token(usuario.id)
    resp = make_response(jsonify({"mensagem": "Login bem-sucedido"}))
    resp.set_cookie('token', token, httponly=True, samesite='Lax')
    return resp

# Rota para verificar se o usuário está logado
@auth_bp.route('/api/usuario-logado', methods=['GET'])
@login_requerido
def usuario_logado():
    usuario = obter_usuario_logado()
    if usuario:
        return jsonify({
            'id': usuario.id,
            'codigo': usuario.codigo_usuario,
            'nome': usuario.nome
        })
    elif getattr(request, 'is_superuser', False):
        return jsonify({
            'id': 0,
            'codigo': 'superuser',
            'nome': 'Administrador'
        })
    return jsonify({'erro': 'Usuário não encontrado'}), 404

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models import Usuario, LogAuditoria, Projeto  
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.auth.auth_utils import login_requerido, obter_usuario_logado
import json

usuario_bp = Blueprint('usuario_bp', __name__)

# ✅ ROTA PARA LISTA DE USUÁRIOS CADASTRADOS
@usuario_bp.route('/usuario')
def usuario():
    resultados = Usuario.query.filter_by(ativo=True).order_by(Usuario.codigo_usuario).all()
    return render_template('admin/usuario.html', resultados=resultados)

# ✅ ROTA PARA CADASTRAR USUÁRIO
@usuario_bp.route('/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    codigo = request.form['codigoUsuario']
    nome = request.form['nomeUsuario']
    email = request.form.get('emailUsuario', None)
    telefone = request.form.get('telefoneUsuario', None)

    usuario_existente = Usuario.query.filter_by(codigo_usuario=codigo).first()
    if usuario_existente:
        return "Usuário já cadastrado. Por favor, escolha outro código.", 400

    try:
        novo_usuario = Usuario(
            codigo_usuario=codigo,
            nome_usuario=nome,
            email=email,
            telefone=telefone
        )
        db.session.add(novo_usuario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar usuário: {str(e)}", 500

    return redirect(url_for('usuario_bp.usuario'))

# ✅ ROTA PARA EDITAR USUÁRIO
@usuario_bp.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfil(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome_usuario = request.form['nomeCompleto']
        usuario.email = request.form.get('emailUsuario')
        usuario.telefone = request.form.get('telefoneUsuario')

        # Atualiza os projetos associados
        ids_projetos = request.form.getlist('projetosSelecionados[]')
        usuario.projetos = Projeto.query.filter(Projeto.id.in_(ids_projetos)).all()

        # 🔐 Atualiza a senha, se fornecida
        nova_senha = request.form.get('novaSenha')
        confirmar_senha = request.form.get('confirmarSenha')

        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                flash('As senhas não coincidem.', 'error')
                return redirect(url_for('usuario_bp.perfil', id=id))
            usuario.senha_hash = generate_password_hash(nova_senha)

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('usuario_bp.usuario'))

    # Carrega todos os projetos e os projetos do usuário
    todos_projetos = Projeto.query.all()
    projetos_usuario_ids = [p.id for p in usuario.projetos]

    return render_template(
        'admin/perfil.html',
        usuario=usuario,
        todos_projetos=todos_projetos,
        projetos_usuario_ids=projetos_usuario_ids
    )

# ✅ ROTA PARA EXCLUIR USUÁRIO
@usuario_bp.route('/excluir-usuario/<int:id>', methods=['POST'])
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    log = LogAuditoria(
        tabela='usuario',
        acao='exclusao',
        id_registro=usuario.id,
        dados_anteriores=json.dumps({
            'codigo_usuario': usuario.codigo_usuario,
            'nome_usuario': usuario.nome_usuario,
            'email': usuario.email,
            'telefone': usuario.telefone
        }),
        data_acao=datetime.now()
    )

    db.session.add(log)
    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for('usuario_bp.usuario'))

# ✅ ROTA PARA VERIFICAR SE O USUÁRIO JÁ ESTÁ CADASTRADO
@usuario_bp.route('/verificar-usuario', methods=['POST'])
def verificar_usuario():
    codigo = request.json.get('codigoUsuario')
    usuario = Usuario.query.filter_by(codigo_usuario=codigo).first()

    if usuario:
        return jsonify({'existe': True, 'mensagem': 'Usuário já cadastrado.'})
    return jsonify({'existe': False})


# ✅ ROTA PARA VERIFICAR MEU PERFIL
@usuario_bp.route('/meu-perfil', methods=['GET', 'POST'])
@login_requerido
def meu_perfil():
    usuario = obter_usuario_logado()  # ← Aqui você pega o usuário logado via JWT

    if request.method == 'POST':
        usuario.nome_usuario = request.form['nomeCompleto']
        usuario.email = request.form.get('emailUsuario')
        usuario.telefone = request.form.get('telefoneUsuario')

        nova_senha = request.form.get('novaSenha')
        confirmar_senha = request.form.get('confirmarSenha')
        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                flash('As senhas não coincidem.', 'error')
                return redirect(url_for('usuario_bp.meu_perfil'))
            usuario.senha_hash = generate_password_hash(nova_senha)

        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('usuario_bp.meu_perfil'))

    # Carrega os projetos para exibir no formulário
    todos_projetos = Projeto.query.all()
    projetos_usuario_ids = [p.id for p in usuario.projetos]
    return render_template(
        'admin/meu_perfil.html',
        usuario=usuario,
        todos_projetos=todos_projetos,
        projetos_usuario_ids=projetos_usuario_ids
    )

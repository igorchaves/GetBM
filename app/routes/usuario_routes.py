from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import Usuario, LogAuditoria, Projeto  # Adicionado Projeto
from app import db
from datetime import datetime
import json

usuario_bp = Blueprint('usuario_bp', __name__)

# ✅ ROTA PARA LISTA DE USUÁRIOS CADASTRADOS
@usuario_bp.route('/usuario')
def usuario():
    resultados = Usuario.query.filter_by(ativo=True).order_by(Usuario.codigo_usuario).all()
    return render_template('usuario.html', resultados=resultados)

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

        db.session.commit()
        return redirect(url_for('usuario_bp.usuario'))

    # Carrega todos os projetos e os projetos do usuário
    todos_projetos = Projeto.query.all()
    projetos_usuario_ids = [p.id for p in usuario.projetos]

    return render_template(
        'perfil.html',
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
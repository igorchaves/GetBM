import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models import Sprint, Usuario, LogAuditoria, Projeto, Backlog, Seguimento
from sqlalchemy import func

from app import db

app = Blueprint('app', __name__, template_folder='../templates')

@app.route('/')
def index():
    resultados = []
    return render_template('index.html', resultados=resultados)

@app.route('/backlog')
def backlog():
    return render_template('backlog.html')

@app.route('/funcionalidades')
def funcionalidades():
    return render_template('funcionalidades.html')

@app.route('/projeto')
def projeto():
    return render_template('projeto.html')

@app.route('/categoria')
def categoria():
    return render_template('categoria.html')

@app.route('/status')
def status():
    return render_template('status.html')

# ✅ ROTA PARA LISTA DE USUÁRIOS CADASTRADOS
@app.route('/usuario')
def usuario():
    resultados = Usuario.query.filter_by(ativo=True).order_by(Usuario.codigo_usuario).all()
    return render_template('usuario.html', resultados=resultados)

# ✅ ROTA PARA CADASTRAR USUÁRIO
@app.route('/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    codigo = request.form['codigoUsuario']
    nome = request.form['nomeUsuario']
    email = request.form.get('emailUsuario', None)
    telefone = request.form.get('telefoneUsuario', None)

    # ✅ Verificação no backend
    usuario_existente = Usuario.query.filter_by(codigo_usuario=codigo).first()
    if usuario_existente:
        # Aqui você pode redirecionar de volta com uma mensagem flash, ou retornar um erro amigável
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

    return redirect(url_for('app.usuario'))

# ✅ ROTA PARA EDITAR USUÁRIO
@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfil(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nome_usuario = request.form['nomeCompleto']
        usuario.email = request.form.get('emailUsuario')
        usuario.telefone = request.form.get('telefoneUsuario')
        db.session.commit()
        return redirect(url_for('app.usuario'))

    return render_template('perfil.html', usuario=usuario)

@app.route('/excluir-usuario/<int:id>', methods=['POST'])
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

    return redirect(url_for('app.usuario'))

# ✅ ROTA PARA VERIFICAR SE O USUÁRIO JÁ ESTÁ CADASTRADO
@app.route('/verificar-usuario', methods=['POST'])
def verificar_usuario():
    codigo = request.json.get('codigoUsuario')
    usuario = Usuario.query.filter_by(codigo_usuario=codigo).first()
    if usuario:
        return jsonify({'existe': True, 'mensagem': 'Usuário já cadastrado.'})
    return jsonify({'existe': False})

# ✅ ROTA PARA LISTAR SPRINTS ATIVAS
@app.route('/sprint')
def sprint():
    sprints = Sprint.query.filter_by(ativo=True).order_by(Sprint.data_inicio.desc()).all()
    return render_template('sprint.html', sprints=sprints)

# ✅ ROTA PARA CADASTRAR SPRINT
@app.route('/cadastrar-sprint', methods=['POST'])
def cadastrar_sprint():
    nome = request.form['sprint']
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
    duracao = int(request.form['duracao'])

    nova_sprint = Sprint(nome=nome, data_inicio=data_inicio, duracao=duracao)
    db.session.add(nova_sprint)
    db.session.commit()

    return redirect(url_for('app.sprint'))

# ✅ ROTA PARA EXCLUSÃO LÓGICA DE SPRINT (mantida como está)
@app.route('/excluir-sprint/<int:id>', methods=['POST'])
def excluir_sprint(id):
    sprint = Sprint.query.get_or_404(id)
    sprint.ativo = False
    db.session.commit()
    return redirect(url_for('app.sprint'))

# ✅ ROTA PARA INCLUSÃO DE PROJETO
@app.route('/cadastrar-projeto', methods=['POST'])
def cadastrar_projeto():
    try:
        codigo = request.form['codigo_projeto']
        nome = request.form['nome_projeto']
        vertical = request.form['vertical']
        backlogs = request.form.getlist('backlogs[]')
        jornadas = request.form.getlist('jornadas[]')

        # ✅ Verificação redundante no backend
        mensagens = []

        if Projeto.query.filter_by(codigo_projeto=codigo).first():
            mensagens.append("Código do projeto já existe.")

        for item in backlogs:
            if Backlog.query.filter_by(descricao=item).first():
                mensagens.append(f"Backlog '{item}' já existe.")

        for item in jornadas:
            if Seguimento.query.filter_by(descricao=item).first():
                mensagens.append(f"Seguimento '{item}' já existe.")

        # ✅ Validação opcional: listas vazias
        if not backlogs:
            mensagens.append("É necessário adicionar pelo menos um backlog.")
        if not jornadas:
            mensagens.append("É necessário adicionar pelo menos um seguimento.")

        if mensagens:
            flash(" | ".join(mensagens), 'danger')
            return redirect(url_for('app.projeto'))

        # ✅ Inserção no banco
        projeto = Projeto(codigo_projeto=codigo, nome_projeto=nome, vertical=vertical)
        db.session.add(projeto)
        db.session.flush()

        for item in backlogs:
            db.session.add(Backlog(descricao=item, projeto_id=projeto.id))

        for item in jornadas:
            db.session.add(Seguimento(descricao=item, projeto_id=projeto.id))

        db.session.commit()
        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('app.projeto'))  # ✅ rota corrigida

    except Exception as e:
        db.session.rollback()
        print(f"[ERRO] Falha ao cadastrar projeto: {str(e)}")  # ✅ log para debug
        flash(f'Erro ao cadastrar projeto: {str(e)}', 'danger')
        return redirect(url_for('app.projeto'))  # ✅ rota corrigida
    
# ✅ ROTA PARA VERIFICAR SE O CÓDIGO DO PROJETO JÁ EXISTE
@app.route('/verificar-projeto', methods=['POST'])
def verificar_projeto():
    try:
        data = request.get_json()
        codigo = data.get('codigoProjeto')
        backlogs = data.get('backlogs', [])
        jornadas = data.get('jornadas', [])

        print("Backlogs recebidos:", backlogs)

        mensagens = []

        if Projeto.query.filter_by(codigo_projeto=codigo).first():
            mensagens.append("Código do projeto já existe.")

        for item in backlogs:
            if Backlog.query.filter(func.lower(Backlog.descricao) == item.lower()).first():
                mensagens.append(f"Backlog '{item}' já existe.")

        for item in jornadas:
            if Seguimento.query.filter(func.lower(Seguimento.descricao) == item.lower()).first():
                mensagens.append(f"Seguimento '{item}' já existe.")

        if mensagens:
            return jsonify({'existe': True, 'mensagem': ' | '.join(mensagens)})

        return jsonify({'existe': False})

    except Exception as e:
        print(f"[ERRO] Falha na verificação do projeto: {str(e)}")
        return jsonify({'existe': False, 'mensagem': 'Erro interno no servidor'}), 500

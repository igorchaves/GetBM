from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models import Projeto, Backlog, Seguimento
from sqlalchemy import func
from app import db

projeto_bp = Blueprint('projeto_bp', __name__)

# Rota principal da página de projeto
@projeto_bp.route('/projeto')
def projeto():
    projetos = Projeto.query.all()
    resultados = []

    for projeto in projetos:
        backlogs = [b.descricao for b in Backlog.query.filter_by(projeto_id=projeto.id).all()]
        jornadas = [j.descricao for j in Seguimento.query.filter_by(projeto_id=projeto.id).all()]

        resultados.append({
            'id': projeto.id,
            'codigo': projeto.codigo_projeto,
            'nome': projeto.nome_projeto,
            'vertical': projeto.vertical,
            'backlogs': backlogs,
            'jornadas': jornadas
        })

    return render_template('admin/projeto.html', resultados=resultados)

# Rota para acessar a página de cadastro de projeto
@projeto_bp.route('/add_projeto')
def add_projeto():
    return render_template('admin/add_projeto.html')

# Rota para cadastrar novo projeto
@projeto_bp.route('/cadastrar-projeto', methods=['POST'])
def cadastrar_projeto():
    try:
        codigo = request.form['codigo_projeto']
        nome = request.form['nome_projeto']
        vertical = request.form['vertical']
        backlogs = request.form.getlist('backlogs[]')
        jornadas = request.form.getlist('jornadas[]')

        mensagens = []

        if Projeto.query.filter_by(codigo_projeto=codigo).first():
            mensagens.append("Código do projeto já existe.")

        for item in backlogs:
            if Backlog.query.filter_by(descricao=item).first():
                mensagens.append(f"Backlog '{item}' já existe.")

        for item in jornadas:
            if Seguimento.query.filter_by(descricao=item).first():
                mensagens.append(f"Seguimento '{item}' já existe.")

        if not backlogs:
            mensagens.append("É necessário adicionar pelo menos um backlog.")
        if not jornadas:
            mensagens.append("É necessário adicionar pelo menos um seguimento.")

        if mensagens:
            flash(" | ".join(mensagens), 'danger')
            return redirect(url_for('projeto_bp.projeto'))

        projeto = Projeto(codigo_projeto=codigo, nome_projeto=nome, vertical=vertical)
        db.session.add(projeto)
        db.session.flush()

        for item in backlogs:
            db.session.add(Backlog(descricao=item, projeto_id=projeto.id))

        for item in jornadas:
            db.session.add(Seguimento(descricao=item, projeto_id=projeto.id))

        db.session.commit()
        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('projeto_bp.projeto'))

    except Exception as e:
        db.session.rollback()
        print(f"[ERRO] Falha ao cadastrar projeto: {str(e)}")
        flash(f'Erro ao cadastrar projeto: {str(e)}', 'danger')
        return redirect(url_for('projeto_bp.projeto'))
    
# Rota para excluir projeto e seus dados relacionados
@projeto_bp.route('/deletar-projeto/<int:id>', methods=['POST'])
def deletar_projeto(id):
    try:
        projeto = Projeto.query.get_or_404(id)

        # Exclui os backlogs e seguimentos relacionados
        Backlog.query.filter_by(projeto_id=projeto.id).delete()
        Seguimento.query.filter_by(projeto_id=projeto.id).delete()

        # Agora exclui o projeto
        db.session.delete(projeto)
        db.session.commit()

        flash('Projeto e dados relacionados excluídos com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir projeto: {str(e)}', 'danger')

    return redirect(url_for('projeto_bp.projeto'))

# Rota para verificação AJAX
@projeto_bp.route('/verificar-projeto', methods=['POST'])
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
    


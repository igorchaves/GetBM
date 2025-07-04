from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Sprint
from app import db
from datetime import datetime

sprint_bp = Blueprint('sprint_bp', __name__)

# ✅ ROTA PARA LISTAR SPRINTS ATIVAS
@sprint_bp.route('/sprint')
def sprint():
    sprints = Sprint.query.filter_by(ativo=True).order_by(Sprint.data_inicio.desc()).all()
    return render_template('sprint.html', sprints=sprints)

# ✅ ROTA PARA CADASTRAR SPRINT
@sprint_bp.route('/cadastrar-sprint', methods=['POST'])
def cadastrar_sprint():
    nome = request.form['sprint']
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
    duracao = int(request.form['duracao'])

    nova_sprint = Sprint(nome=nome, data_inicio=data_inicio, duracao=duracao)
    db.session.add(nova_sprint)
    db.session.commit()

    return redirect(url_for('sprint_bp.sprint'))

# ✅ ROTA PARA EXCLUSÃO LÓGICA DE SPRINT
@sprint_bp.route('/excluir-sprint/<int:id>', methods=['POST'])
def excluir_sprint(id):
    sprint = Sprint.query.get_or_404(id)
    sprint.ativo = False
    db.session.commit()
    return redirect(url_for('sprint_bp.sprint'))

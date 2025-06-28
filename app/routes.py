from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Sprint
from app import db
from datetime import datetime

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

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# 🆕 ROTA PARA LISTAR SPRINTS ATIVAS
@app.route('/sprint')
def sprint():
    sprints = Sprint.query.filter_by(ativo=True).order_by(Sprint.data_inicio.desc()).all()
    return render_template('sprint.html', sprints=sprints)

# 🆕 ROTA PARA CADASTRAR SPRINT
@app.route('/cadastrar-sprint', methods=['POST'])
def cadastrar_sprint():
    nome = request.form['sprint']
    data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date()
    duracao = int(request.form['duracao'])

    nova_sprint = Sprint(nome=nome, data_inicio=data_inicio, duracao=duracao)
    db.session.add(nova_sprint)
    db.session.commit()

    return redirect(url_for('app.sprint'))

# 🆕 ROTA PARA EXCLUSÃO LÓGICA DE SPRINT
@app.route('/excluir-sprint/<int:id>', methods=['POST'])
def excluir_sprint(id):
    sprint = Sprint.query.get_or_404(id)
    sprint.ativo = False
    db.session.commit()
    return redirect(url_for('app.sprint'))

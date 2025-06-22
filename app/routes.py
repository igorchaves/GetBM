from flask import Blueprint, render_template

app = Blueprint('app', __name__, template_folder='../templates')

@app.route('/')
def index():
    resultados = []  # ou dados simulados
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

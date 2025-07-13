from flask import Blueprint, render_template
from app.auth.auth_utils import login_requerido
from flask import redirect
import logging
logging.basicConfig(level=logging.DEBUG)

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def redirecionar_para_login():
    return redirect('/auth/login')

@home_bp.route('/home')
@login_requerido
def index():
    logging.debug(">>> Entrou na rota /home")
    return render_template('home/index.html')

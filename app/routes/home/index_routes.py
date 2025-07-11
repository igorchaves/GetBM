from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def login():
    return render_template('home/login.html')

@home_bp.route('/home')
def index():
    return render_template('home/index.html')  # ou outra página inicial


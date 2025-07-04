from flask import Blueprint, render_template

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categoria')
def categoria():
    return render_template('categoria.html')

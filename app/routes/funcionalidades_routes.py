from flask import Blueprint, render_template

funcionalidades_bp = Blueprint('funcionalidades_bp', __name__)

@funcionalidades_bp.route('/funcionalidades')
def funcionalidades():
    return render_template('configuration/funcionalidades.html')

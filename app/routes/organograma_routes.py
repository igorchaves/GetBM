from flask import Blueprint, render_template

organograma_bp = Blueprint('organograma_bp', __name__)

@organograma_bp.route('/organograma')
def organograma():
    return render_template('management/organograma.html')

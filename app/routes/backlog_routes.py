from flask import Blueprint, render_template

backlog_bp = Blueprint('backlog_bp', __name__)

@backlog_bp.route('/backlog')
def backlog():
    return render_template('backlog.html')

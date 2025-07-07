from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Status

status_bp = Blueprint('status_bp', __name__)

# Rota de navegação (já funcional)
@status_bp.route('/status')
def status():
    return render_template('configuration/status.html', status_list=[])

# Rota para listar todos os status
@status_bp.route('/status/listar', methods=['GET'])
def listar_status():
    status_list = Status.query.all()
    return jsonify([
        {'id': s.id, 'codigo': s.codigo, 'nome': s.nome}
        for s in status_list
    ])

# Rota para adicionar novo status
@status_bp.route('/status/adicionar', methods=['POST'])
def adicionar_status():
    data = request.get_json()
    novo_status = Status(codigo=data['codigo'], nome=data['nome'])
    db.session.add(novo_status)
    db.session.commit()
    return jsonify({'mensagem': 'Status adicionado com sucesso'})

# Rota para deletar status
@status_bp.route('/status/deletar/<int:id>', methods=['DELETE'])
def deletar_status(id):
    status = Status.query.get(id)
    if not status:
        return jsonify({'erro': 'Status não encontrado'}), 404
    db.session.delete(status)
    db.session.commit()
    return jsonify({'mensagem': 'Status excluído com sucesso'})

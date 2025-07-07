from flask import Blueprint, request, jsonify
from app import db
from app.models import Sprint
from datetime import datetime

api_sprint_bp = Blueprint('api_sprint_bp', __name__)

# ✅ GET: Listar sprints ativas
@api_sprint_bp.route('/api/sprints', methods=['GET'])
def listar_sprints():
    sprints = Sprint.query.filter_by(ativo=True).order_by(Sprint.data_inicio.desc()).all()
    return jsonify([s.to_dict() for s in sprints])

# ✅ POST: Cadastrar nova sprint
@api_sprint_bp.route('/api/sprints', methods=['POST'])
def cadastrar_sprint():
    data = request.json
    try:
        nome = data['sprint']
        data_inicio = datetime.strptime(data['data_inicio'], '%Y-%m-%d').date()
        duracao = int(data['duracao'])

        nova_sprint = Sprint(nome=nome, data_inicio=data_inicio, duracao=duracao)
        db.session.add(nova_sprint)
        db.session.commit()

        return jsonify({'message': 'Sprint cadastrada com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ✅ DELETE: Exclusão lógica de sprint
@api_sprint_bp.route('/api/sprints/<int:id>', methods=['DELETE'])
def excluir_sprint(id):
    sprint = Sprint.query.get_or_404(id)
    sprint.ativo = False
    db.session.commit()
    return jsonify({'message': 'Sprint excluída com sucesso'})

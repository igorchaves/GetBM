from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.configuration.categorias_model import Categoria  # ajuste conforme o nome real do model

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categoria')
def categoria():
    return render_template('configuration/categoria.html')

# Rota para listar categorias (GET)
@categoria_bp.route('/api/categorias', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.order_by(Categoria.id.asc()).all()
    return jsonify([
        {"id": c.id, "codigo": c.codigo, "nome": c.nome}
        for c in categorias
    ])

# Rota para adicionar nova categoria (POST)
@categoria_bp.route('/api/categorias', methods=['POST'])
def adicionar_categoria():
    data = request.json
    nova_categoria = Categoria(
        codigo=data.get('codigo'),
        nome=data.get('nome')
    )
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify({"message": "Categoria adicionada com sucesso!"}), 201

# Rota para excluir categoria (DELETE)
@categoria_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
def excluir_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoria excluída com sucesso!"})

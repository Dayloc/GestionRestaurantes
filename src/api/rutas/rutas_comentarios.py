from flask import Blueprint, request, jsonify
from api.models import Comentario

comm = Blueprint("comm", __name__, url_prefix="/comm")

# GET: Listar comentarios
@comm.route("/", methods=["GET"])
def get_comentarios():
    return jsonify([c.to_dict() for c in Comentario.listar()]), 200

# GET: Comentario por ID
@comm.route("/<int:coment_id>", methods=["GET"])
def get_comentario(coment_id):
    c = Comentario.get_by_id(coment_id)
    if not c:
        return jsonify({"error": "Comentario no encontrado"}), 404
    return jsonify(c.to_dict()), 200

# POST: Crear comentario
@comm.route("/", methods=["POST"])
def create_comentario():
    data = request.get_json()
    required_fields = ["texto", "post_id", "user_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo {field}"}), 400
    nuevo = Comentario.crear(
        texto=data["texto"],
        post_id=data["post_id"],
        user_id=data["user_id"]
    )
    return jsonify(nuevo.to_dict()), 201

# PUT: Actualizar comentario
@comm.route("/<int:coment_id>", methods=["PUT"])
def update_comentario(coment_id):
    c = Comentario.get_by_id(coment_id)
    if not c:
        return jsonify({"error": "Comentario no encontrado"}), 404
    data = request.get_json()
    c.actualizar(**data)
    return jsonify(c.to_dict()), 200

# DELETE: Eliminar comentario
@comm.route("/<int:coment_id>", methods=["DELETE"])
def delete_comentario(coment_id):
    c = Comentario.get_by_id(coment_id)
    if not c:
        return jsonify({"error": "Comentario no encontrado"}), 404
    c.eliminar()
    return jsonify({"msg": f"Comentario {coment_id} eliminado"}), 200

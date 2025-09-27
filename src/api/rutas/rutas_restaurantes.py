from flask import Blueprint, request, jsonify
from api.models import Restaurant

rest = Blueprint("rest", __name__, url_prefix="/rest")

# GET: Listar todos los restaurantes
@rest.route("/", methods=["GET"])
def get_restaurantes():
    return jsonify([r.to_dict() for r in Restaurant.listar()]), 200

# GET: Restaurante por ID
@rest.route("/<int:rest_id>", methods=["GET"])
def get_restaurante(rest_id):
    r = Restaurant.get_by_id(rest_id)
    if not r:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    return jsonify(r.to_dict()), 200

# POST: Crear restaurante
@rest.route("/", methods=["POST"])
def create_restaurante():
    data = request.get_json()
    required_fields = ["nombre", "cantidad_trabajadores", "localizacion"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo {field}"}), 400
    nuevo = Restaurant.crear(
        nombre=data["nombre"],
        cantidad_trabajadores=data["cantidad_trabajadores"],
        localizacion=data["localizacion"]
    )
    return jsonify(nuevo.to_dict()), 201

# PUT: Actualizar restaurante
@rest.route("/<int:rest_id>", methods=["PUT"])
def update_restaurante(rest_id):
    r = Restaurant.get_by_id(rest_id)
    if not r:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    data = request.get_json()
    r.actualizar(**data)
    return jsonify(r.to_dict()), 200

# DELETE: Eliminar restaurante
@rest.route("/<int:rest_id>", methods=["DELETE"])
def delete_restaurante(rest_id):
    r = Restaurant.get_by_id(rest_id)
    if not r:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    r.eliminar()
    return jsonify({"msg": f"Restaurante {rest_id} eliminado"}), 200

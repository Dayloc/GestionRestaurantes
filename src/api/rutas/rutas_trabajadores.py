from flask import Blueprint, request, jsonify
from api.models import Trabajador
import bcrypt

trab = Blueprint("trab", __name__, url_prefix="/trab")

# GET: Listar todos
@trab.route("/", methods=["GET"])
def get_trabajadores():
    result = []
    for t in Trabajador.listar():
        dic = t.to_dict()
        dic.pop("password", None)
        result.append(dic)
    return jsonify(result), 200

# GET: Por ID
@trab.route("/<int:trab_id>", methods=["GET"])
def get_trabajador(trab_id):
    t = Trabajador.get_by_id(trab_id)
    if not t:
        return jsonify({"error": "Trabajador no encontrado"}), 404
    dic = t.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 200

# POST: Crear trabajador
@trab.route("/", methods=["POST"])
def create_trabajador():
    data = request.get_json()
    required_fields = ["nombre", "primer_apellido", "email", "password", "restaurant_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo {field}"}), 400

    # Hashear contraseña
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")

    nuevo = Trabajador.crear(
        nombre=data["nombre"],
        primer_apellido=data["primer_apellido"],
        email=data["email"],
        password=password_hash,
        restaurant_id=data["restaurant_id"]
    )
    dic = nuevo.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 201

# PUT: Actualizar trabajador
@trab.route("/<int:trab_id>", methods=["PUT"])
def update_trabajador(trab_id):
    t = Trabajador.get_by_id(trab_id)
    if not t:
        return jsonify({"error": "Trabajador no encontrado"}), 404
    data = request.get_json()
    if "password" in data:
        salt = bcrypt.gensalt(rounds=12)
        data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")
    t.actualizar(**data)
    dic = t.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 200

# DELETE: Eliminar trabajador
@trab.route("/<int:trab_id>", methods=["DELETE"])
def delete_trabajador(trab_id):
    t = Trabajador.get_by_id(trab_id)
    if not t:
        return jsonify({"error": "Trabajador no encontrado"}), 404
    t.eliminar()
    return jsonify({"msg": f"Trabajador {trab_id} eliminado"}), 200

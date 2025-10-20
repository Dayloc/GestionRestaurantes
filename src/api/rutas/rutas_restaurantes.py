from flask import Blueprint, request, jsonify
from api.models import Restaurant
from flask_jwt_extended import create_access_token
import bcrypt

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
@rest.route("/register", methods=["POST"])
def create_restaurante():
    data = request.get_json()
    
    # Revisar que data no sea None
    if not data:
        return jsonify({"error": "JSON inválido o no enviado"}), 400

    required_fields = ["nombre", "cantidad_trabajadores", "localizacion", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo {field}"}), 400

    # Hashear contraseña
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")

    nuevo = Restaurant.crear(
        nombre=data["nombre"],
        cantidad_trabajadores=data["cantidad_trabajadores"],
        localizacion=data["localizacion"],
        email=data["email"],
        password=password_hash
    )

    dic = nuevo.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 201

# PUT: Actualizar restaurante
@rest.route("/<int:rest_id>", methods=["PUT"])
def update_restaurante(rest_id):
    r = Restaurant.get_by_id(rest_id)
    if not r:
        return jsonify({"error": "Restaurante no encontrado"}), 404

    data = request.get_json()
    if "password" in data:
        salt = bcrypt.gensalt()
        data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")

    r.actualizar(**data)
    dic = r.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 200

# DELETE: Eliminar restaurante
@rest.route("/<int:rest_id>", methods=["DELETE"])
def delete_restaurante(rest_id):
    r = Restaurant.get_by_id(rest_id)
    if not r:
        return jsonify({"error": "Restaurante no encontrado"}), 404
    r.eliminar()
    return jsonify({"msg": f"Restaurante {rest_id} eliminado"}), 200


# LOGIN RESTAURANTE
@rest.route("/login", methods=["POST"])
def login_restaurante():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    restaurante = Restaurant.query.filter_by(email=email).first()
    if not restaurante:
        return jsonify({"error": "Restaurante no encontrado"}), 404

    if not bcrypt.checkpw(password.encode("utf-8"), restaurante.password.encode("utf-8")):
        return jsonify({"error": "La contraseña no es correcta"}), 401

    token = create_access_token(identity={"id": restaurante.id, "rol": "restaurant"})

    dic = restaurante.to_dict()
    dic.pop("password", None)
    return jsonify({
        "msg": "Login exitoso",
        "token": token,
        "restaurant": dic
    }), 200
from flask import Blueprint, request, jsonify
from api.models import Cliente
import bcrypt

clien = Blueprint('clien', __name__, url_prefix="/clien")

# GET: Listar todos los clientes
@clien.route("/", methods=["GET"])
def get_clientes():
    clientes = Cliente.listar()
    result = []
    for c in clientes:
        dic = c.to_dict()
        dic.pop("password", None)  # No devolver contraseña
        result.append(dic)
    return jsonify(result), 200

# GET: Obtener un cliente por id
@clien.route("/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):
    cliente = Cliente.get_by_id(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    dic = cliente.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 200

# POST: Crear cliente
@clien.route("/", methods=["POST"])
def create_cliente():
    data = request.get_json()
    required_fields = ["nombre", "primer_apellido", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Falta el campo {field}"}), 400

    # Hashear contraseña
    salt = bcrypt.gensalt(rounds=12)
    pass_encrip = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")

    nuevo_cliente = Cliente.crear(
        nombre=data["nombre"],
        primer_apellido=data["primer_apellido"],
        email=data["email"],
        password=pass_encrip
    )

    dic = nuevo_cliente.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 201

# PUT: Actualizar cliente
@clien.route("/<int:cliente_id>", methods=["PUT"])
def update_cliente(cliente_id):
    cliente = Cliente.get_by_id(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    data = request.get_json()
    # Si viene contraseña, la hasheamos
    if "password" in data:
        salt = bcrypt.gensalt(rounds=12)
        data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), salt).decode("utf-8")

    cliente.actualizar(**data)
    dic = cliente.to_dict()
    dic.pop("password", None)
    return jsonify(dic), 200

# DELETE: Eliminar cliente
@clien.route("/<int:cliente_id>", methods=["DELETE"])
def delete_cliente(cliente_id):
    cliente = Cliente.get_by_id(cliente_id)
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404

    cliente.eliminar()
    return jsonify({"msg": f"Cliente {cliente_id} eliminado"}), 200

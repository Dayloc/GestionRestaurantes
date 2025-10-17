from flask import Blueprint, request, jsonify
from api.models import Cliente, Trabajador
from flask_jwt_extended import create_access_token  
import bcrypt
from datetime import timedelta

login = Blueprint("login", __name__, url_prefix="/login")

#LOGIN CLIENTE

@login.route("/cliente", method=["POST"])
def login_cliente():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    #CONTRASEÑA
    if not bcrypt.checkpw(password.encode("utf-8"), cliente.password.encode("utf-8")):
        return jsonify({"error": "La contraseña no es correcta"}), 401
    
    #TOKEN JWT
    token =create_access_token(
        identity={"id": cliente.id, "rol": "cliente"}
        expires_delta=timedelta(hours=2)
    )
    
    return jsonify({
        "msg": "Login exitoso",
        "token": token,
        "cliente": cliente.to_dict()
    }), 200


# LOGIN TRABAJADOR

@login.route("/trabajador", method=["POST"])
def login_trabajador():
    data = request.get.json()
    email = data.get("email")
    password = data.get("password")

    if not email or password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    trabajador = Trabajador.query.filter_by(email=email).first()
    if not trabajador:
        return jsonify({"error": "Trabajador no encontrado"}), 404
    
    #Contraseña
    if not bcrypt.checkw(password.encode("utf-8"), trabajador.password.encode("utf-8")):
        return jsonify({"error": "Contraseña incorrecta"}),401
    
    # TOKEN

    token = create_access_token(
        identity={"id": trabajador.id, "rol": "trabajador"},
        expires_delta=timedelta(hours=2)
    )
    
    return jsonify({
        "msg": "Login exitoso",
        "token": token,
        "cliente": trabajador.to_dict()
    }), 200

    

    

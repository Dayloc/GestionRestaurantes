"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.rutas import rest
from api.rutas import clien
from api.rutas import poster
from api.rutas import trab
from api.rutas import comm
from flask_jwt_extended import JWTManager
from api.admin import setup_admin
from api.commands import setup_commands
from datetime import timedelta
from flask_cors import CORS   # ✅ Importar CORS

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../dist/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# ✅ Configurar base de datos
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# ✅ JWT Config
app.config["JWT_SECRET_KEY"] = "nada_es_real_solo_tu_que_te_parece"  # Cámbialo en producción
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)

# ✅ Habilitar CORS (para permitir peticiones desde el frontend)
CORS(app, origins="*", supports_credentials=True)
# Si quieres limitarlo solo al frontend:
# CORS(app, origins=["https://literate-space-couscous-7vwp979jv46php5g9-3000.app.github.dev"], supports_credentials=True)

# ✅ Configurar admin y comandos
setup_admin(app)
setup_commands(app)

# ✅ Registrar blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(rest)
app.register_blueprint(poster)
app.register_blueprint(clien)
app.register_blueprint(trab)
app.register_blueprint(comm)

# ✅ Manejar errores API como JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# ✅ Sitemap para desarrollo
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# ✅ Manejar archivos estáticos
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # evitar cache
    return response


# ✅ Ejecutar servidor
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)

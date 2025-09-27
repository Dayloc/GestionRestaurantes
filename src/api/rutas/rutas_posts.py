from flask import Blueprint, request, jsonify
from api.models import db, Post


poster = Blueprint('poster', __name__, url_prefix="/poster")


# GET Todos
@poster.route("/", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts]), 200


# GET

@poster.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200


# POST

@poster.route("/", methods=["POST"])
def create_post():
    data = request.get_json()
    nuevo_post = Post(
        titulo=data.get("titulo"),
        media=data.get("media"),
        cliente_id=data.get("cliente_id"),
        restaurante_id=data.get("restaurante_id")
    )
    db.session.add(nuevo_post)
    db.session.commit()
    return jsonify(nuevo_post.to_dict()), 201


# PUT

@poster.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.titulo = data.get("titulo", post.titulo)
    post.media = data.get("media", post.media)
    db.session.commit()
    return jsonify(post.to_dict()), 200

# DELETE

@poster.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"msg": f"Post {post_id} eliminado"}), 200

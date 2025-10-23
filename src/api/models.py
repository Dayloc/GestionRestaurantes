from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Column
from typing import List

db = SQLAlchemy()

# --- Tabla intermedia para relación muchos a muchos restaurante-cliente
cliente_restaurant = Table(
    "cliente_restaurant",
    db.Model.metadata,
    Column("restaurant_id", ForeignKey("restaurant.id"), primary_key=True),
    Column("cliente_id", ForeignKey("cliente.id"), primary_key=True)
)


#  Restaurant 

class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    cantidad_trabajadores: Mapped[int] = mapped_column(nullable=False)
    localizacion: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)  

    trabajadores: Mapped[List["Trabajador"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )
    clientes: Mapped[List["Cliente"]] = relationship(
        secondary=cliente_restaurant,
        back_populates="restaurants"
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad_trabajadores": self.cantidad_trabajadores,
            "localizacion": self.localizacion,
            "trabajadores": [t.id for t in self.trabajadores],
            "clientes": [c.id for c in self.clientes],
            "posts": [p.id for p in self.posts],
            "email": self.email,
        }

   
    @classmethod
    def crear(cls, nombre, cantidad_trabajadores, localizacion, email, password):
        nuevo_restaurante = cls(nombre=nombre, cantidad_trabajadores=cantidad_trabajadores, localizacion=localizacion, email=email, password=password)
        db.session.add(nuevo_restaurante)
        db.session.commit()
        return nuevo_restaurante

    @classmethod
    def listar(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def actualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return True



#  Trabajador 

class Trabajador(db.Model):
    __tablename__ = "trabajador"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    primer_apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"))

    restaurant: Mapped["Restaurant"] = relationship(back_populates="trabajadores")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "primer_apellido": self.primer_apellido,
            "email": self.email,
            "restaurant_id": self.restaurant_id
        }

    @classmethod
    def crear(cls, nombre, primer_apellido, email, password, restaurant_id):
        nuevo = cls(
            nombre=nombre,
            primer_apellido=primer_apellido,
            email=email,
            password=password,
            restaurant_id=restaurant_id
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

    @classmethod
    def listar(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def actualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return True



#  Cliente 

class Cliente(db.Model):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    primer_apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        back_populates="autor",
        cascade="all, delete-orphan"
    )
    comentarios: Mapped[List["Comentario"]] = relationship(
        back_populates="autor",
        cascade="all, delete-orphan"
    )
    restaurants: Mapped[List["Restaurant"]] = relationship(
        secondary=cliente_restaurant,
        back_populates="clientes"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "primer_apellido": self.primer_apellido,
            "email": self.email,
            "posts": [p.id for p in self.posts],
            "comentarios": [c.id for c in self.comentarios],
            "restaurants": [r.id for r in self.restaurants]
        }

   
    @classmethod
    def crear(cls, nombre, primer_apellido, email, password):
        nuevo = cls(nombre=nombre, primer_apellido=primer_apellido, email=email, password=password)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

    @classmethod
    def listar(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def actualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return True


#  Post 

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    media: Mapped[str] = mapped_column(String(255), nullable=True)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    restaurante_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"), nullable=False)

    autor: Mapped["Cliente"] = relationship(back_populates="posts")
    restaurant: Mapped["Restaurant"] = relationship(back_populates="posts")
    comentarios: Mapped[List["Comentario"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "media": self.media,
            "cliente_id": self.cliente_id,
            "restaurante_id": self.restaurante_id,
            "comentarios": [c.id for c in self.comentarios]
        }

    
    @classmethod
    def crear(cls, titulo, cliente_id, restaurante_id, media=None):
        nuevo_post = cls(titulo=titulo, media=media, cliente_id=cliente_id, restaurante_id=restaurante_id)
        db.session.add(nuevo_post)
        db.session.commit()
        return nuevo_post

    @classmethod
    def listar(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def actualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return True



#  Comentario 

class Comentario(db.Model):
    __tablename__ = "comentario"

    id: Mapped[int] = mapped_column(primary_key=True)
    texto: Mapped[str] = mapped_column(String(500), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="comentarios")
    autor: Mapped["Cliente"] = relationship(back_populates="comentarios")

    def to_dict(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "post_id": self.post_id,
            "user_id": self.user_id
        }

    
    @classmethod
    def crear(cls, texto, post_id, user_id):
        nuevo_comentario = cls(texto=texto, post_id=post_id, user_id=user_id)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return nuevo_comentario

    @classmethod
    def listar(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def actualizar(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
        return True

import click
from api.models import db, Cliente, Post, Restaurant, Trabajador, Comentario

def setup_commands(app):

    #  Insertar clientes de prueba
    @app.cli.command("insert-test-clients")
    @click.argument("count")
    def insert_test_clients(count):
        print("Creando clientes de prueba...")
        for x in range(1, int(count) + 1):
            cliente = Cliente(
                nombre=f"Cliente{x}",
                primer_apellido=f"Apellido{x}",
                email=f"cliente{x}@test.com",
                password="123456"
            )
            db.session.add(cliente)
        db.session.commit()
        print(f"{count} clientes de prueba creados ✅")

    #  Insertar restaurantes de prueba
    @app.cli.command("insert-test-restaurants")
    @click.argument("count")
    def insert_test_restaurants(count):
        print("Creando restaurantes de prueba...")
        for x in range(1, int(count) + 1):
            restaurant = Restaurant(
                nombre=f"Restaurante{x}",
                cantidad_trabajadores=5,
                localizacion=f"Ciudad{x}"
            )
            db.session.add(restaurant)
        db.session.commit()
        print(f"{count} restaurantes de prueba creados ✅")

    #  Insertar trabajadores de prueba
    @app.cli.command("insert-test-trabajadores")
    @click.argument("count")
    def insert_test_trabajadores(count):
        print("Creando trabajadores de prueba...")
        restaurants = Restaurant.query.all()
        if not restaurants:
            print("⚠️ No hay restaurantes, crea algunos primero con: flask insert-test-restaurants N")
            return

        for x in range(1, int(count) + 1):
            trabajador = Trabajador(
                nombre=f"Trabajador{x}",
                primer_apellido=f"Apellido{x}",
                email=f"trabajador{x}@test.com",
                password="123456",
                restaurant_id=restaurants[x % len(restaurants)].id  # se asignan a restaurantes existentes
            )
            db.session.add(trabajador)
        db.session.commit()
        print(f"{count} trabajadores de prueba creados ✅")

    #  Insertar posts de prueba
    @app.cli.command("insert-test-posts")
    @click.argument("count")
    def insert_test_posts(count):
        print("Creando posts de prueba...")
        clientes = Cliente.query.all()
        restaurants = Restaurant.query.all()

        if not clientes or not restaurants:
            print("⚠️ Necesitas clientes y restaurantes primero")
            return

        for x in range(1, int(count) + 1):
            post = Post(
                titulo=f"Post de prueba {x}",
                media=None,
                cliente_id=clientes[x % len(clientes)].id,
                restaurante_id=restaurants[x % len(restaurants)].id
            )
            db.session.add(post)
        db.session.commit()
        print(f"{count} posts de prueba creados ✅")

    #  Insertar comentarios de prueba
    @app.cli.command("insert-test-comentarios")
    @click.argument("count")
    def insert_test_comentarios(count):
        print("Creando comentarios de prueba...")
        clientes = Cliente.query.all()
        posts = Post.query.all()

        if not clientes or not posts:
            print("⚠️ Necesitas clientes y posts primero")
            return

        for x in range(1, int(count) + 1):
            comentario = Comentario(
                texto=f"Comentario de prueba {x}",
                post_id=posts[x % len(posts)].id,
                user_id=clientes[x % len(clientes)].id
            )
            db.session.add(comentario)
        db.session.commit()
        print(f"{count} comentarios de prueba creados ✅")

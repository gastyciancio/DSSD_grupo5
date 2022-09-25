from os import environ
from flask import Flask, render_template, redirect, url_for, session
from config import config
from app import db
from app.resources import coleccion
from app.resources import auth
from flask_cors import CORS
from app.helpers import auth as helper_auth
from app.resources import usuario
from app.helpers import handler
from app.helpers.auth import authenticated



def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)
    CORS(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    

    # Configure db
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    #app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
     # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    # app.jinja_env.globals.update(isAdmin=helper_auth.isAdmin)
    app.jinja_env.globals.update(tiene_permiso=helper_auth.check_permission)
    
    # Rutas de Consultas

    app.add_url_rule("/crear_coleccion","coleccion_create",coleccion.collecion_create, methods=["POST"] )
    app.add_url_rule("/coleccion_index","coleccion_index",coleccion.index, methods=["GET"] )
    app.add_url_rule("/usuarios", "usuario_index", usuario.index, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/nuevo", "usuario_create", usuario.create, methods=["POST"])
    app.add_url_rule("/usuarios/update/<int:id>","usuario_update", usuario.update,methods=["POST", "GET"])
    app.add_url_rule("/usuarios/delete/<int:id>", "usuario_delete", usuario.delete)
    app.add_url_rule("/usuarios/show/<int:id>", "usuario_show", usuario.show)
    app.add_url_rule("/usuarios/perfil", "usuario_perfil", usuario.verPerfil)
    app.add_url_rule("/usuarios/perfilUpdate/<int:id>","usuario_update_perfil",usuario.updatePerfil,methods=["POST", "GET"])
    app.add_url_rule("/usuarios/passwordUpdate/<int:id>","usuario_update_password",usuario.updatePassword,methods=["POST", "GET"])

     # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )


    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        user = authenticated(session)
        if not user:
            return redirect(url_for("auth_login"))
        else:
            return render_template("home.html")
    
    # Rutas de API-REST (usando Blueprints)
   
    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(403, handler.forbidden_error)
    

    
    return app
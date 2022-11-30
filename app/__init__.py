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
from app.models.coleccion import Coleccion
from app.resources import provider
from app.resources import maker
from app.resources import ruta
from app.helpers.bonita_api import get_cases_ids_of_collections_in_task
from app.resources import indicators

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
    app.jinja_env.globals.update(tiene_permiso=helper_auth.check_permission_bonita)
    
    # Rutas de Consultas
    app.add_url_rule("/crear_coleccion","coleccion_create",coleccion.collecion_create, methods=["POST"] )
    app.add_url_rule("/coleccion_index","coleccion_index",coleccion.index, methods=["GET"] )
    app.add_url_rule("/establecer_materiales_y_cantidades","set_materials_and_quantities",coleccion.set_materials_and_quantities, methods=["POST"] )
    app.add_url_rule("/establecer_materiales_y_cantidades_index","set_materials_and_quantities_index",coleccion.set_materials_and_quantities_index, methods=["GET"] )
    app.add_url_rule("/usuarios", "usuario_index", usuario.index, methods=["POST", "GET"])
    app.add_url_rule("/usuarios/nuevo", "usuario_create", usuario.create, methods=["POST"])
    app.add_url_rule("/usuarios/update/<int:id>","usuario_update", usuario.update,methods=["POST", "GET"])
    app.add_url_rule("/usuarios/delete/<int:id>", "usuario_delete", usuario.delete)
    app.add_url_rule("/usuarios/show/<int:id>", "usuario_show", usuario.show)
    app.add_url_rule("/usuarios/perfil", "usuario_perfil", usuario.verPerfil)
    app.add_url_rule("/usuarios/perfilUpdate/<int:id>","usuario_update_perfil",usuario.updatePerfil,methods=["POST", "GET"])
    app.add_url_rule("/usuarios/passwordUpdate/<int:id>","usuario_update_password",usuario.updatePassword,methods=["POST", "GET"])
    app.add_url_rule("/form_proveedores", "providers_form",provider.index, methods=["GET"] )
    app.add_url_rule("/search_proveedores", "providers_search", provider.search ,methods=["POST"])
    app.add_url_rule("/reserve_proveedores", "providers_reserve", provider.reserve ,methods=["POST"])
    app.add_url_rule("/form_fabricantes", "makers_form",maker.index, methods=["GET"] )
    app.add_url_rule("/search_fabricantes", "makers_search", maker.search ,methods=["POST"])
    app.add_url_rule("/reserve_fabricantes", "makers_reserve", maker.reserve ,methods=["POST"])
    app.add_url_rule("/form_rutas", "rutas_form",ruta.index, methods=["GET"] )
    app.add_url_rule("/crear_rutas", "rutas_create", ruta.ruta_create ,methods=["POST"])
    app.add_url_rule("/indicators", "indicators", indicators.index, methods=["GET"])
    app.add_url_rule("/coleccion_ready", "coleccion_ready", coleccion.colecctions_ready, methods=["GET"])
    app.add_url_rule("/lanzar_coleccion/<int:id>", "coleccion_lanzar", coleccion.lanzar, methods=["POST"])


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
            case_id_collections_active = get_cases_ids_of_collections_in_task(name="Establecer materiales y cantidad necesarios")
            collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

            return render_template("home.html", cols=collections)
    
    # Rutas de API-REST (usando Blueprints)
   
    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(403, handler.forbidden_error)
    

    
    return app
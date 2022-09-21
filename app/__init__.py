from os import environ
from flask import Flask, render_template
from config import config
from app import db
from app.resources import coleccion



def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    

    # Configure db
    #db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    #app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    

    # Rutas de Consultas

    app.add_url_rule("/crear_coleccion","coleccion_create",coleccion.collecion_create, methods=["POST"] )


    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return render_template("home.html")
    


    # Rutas de API-REST (usando Blueprints)
   

    # Handlers
    
    

    
    return app
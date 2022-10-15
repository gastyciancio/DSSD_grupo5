from flask import Flask
from db import init_app
#Config
from config import config
from os import environ
from dotenv import load_dotenv
#Models
from app.models.supplier import Supplier
from app.models.material import Material
from app.models.supplier_material import SupplierMaterial
#Routes
from app.controllers.supplier import supplier


load_dotenv()

def create_app(environment = "development"):
    
    app = Flask(__name__)

    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    init_app(app)

    @app.route("/")
    def home():
        suppliers = Supplier.query.all()
        
        for supplier in suppliers:
            print("Nombre del supplier: " + supplier.name, flush=True)
            for sup_mat in supplier.materials:
                print("Material: " + sup_mat.material.name, flush=True)
                print("Precio: " + str(sup_mat.price_per_kg), flush=True)
            print("---------------", flush=True)
        
        return "Home!"

    #Blueprints
    app.register_blueprint(supplier)

    return app
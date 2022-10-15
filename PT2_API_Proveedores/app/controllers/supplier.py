from flask import Blueprint, jsonify
from app.models.supplier import Supplier

supplier = Blueprint("supplier", __name__, url_prefix="/supplier")

@supplier.get("/")
def index():
    suppliers = [ supplier.json() for supplier in Supplier.get_suppliers() ]
    return jsonify({'suppliers': suppliers })
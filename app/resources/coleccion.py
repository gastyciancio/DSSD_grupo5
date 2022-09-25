from flask import redirect, render_template, request, url_for, session, abort
import flask
from flask.helpers import flash
from sqlalchemy.sql.expression import true
#from app.resources.validadorColeccion import ValidarForm
from app.db import db
from app.models.coleccion import Coleccion

def index():
    return render_template("colecciones/colecciones.html")

def collecion_create():
    params=request.form
    nueva_coleccion=Coleccion(nombre=params["model_name"],descripcion=params["description"],fecha=params["fecha"],tipo=params["glasses_type"])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje="Se agrego la coleccion"
    flash(mensaje)
    return redirect(url_for("home"))

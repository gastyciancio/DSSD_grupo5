from flask import redirect, render_template, request, url_for, session, abort
import flask
from flask.helpers import flash
from sqlalchemy.sql.expression import true
#from app.resources.validadorColeccion import ValidarForm
from app import db
from app.models.coleccion import Coleccion

def collecion_create():
    #if not authenticated(session):
     #   abort(401)
    params=request.form
    #cant_puntos=Punto.existe_punto(params["nombre"]) # Me fijo si ya existe un punto con ese nombre
    #if (cant_puntos==0): #si la cantidad es 0 es porque no hay ninguna tupla en la base de datos con ese nombre, o sea que no existe 
    nueva_coleccion=Coleccion(nombre=params["model_name"],descripcion=params["description"],fecha=params["fecha"],tipo=params["glasses_type"])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje="Se agrego la coleccion"
    #else:
    flash(mensaje)
    return redirect(url_for("/"))

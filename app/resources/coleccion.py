from flask import redirect, render_template, request, url_for, session, abort
import flask
from flask.helpers import flash
from sqlalchemy.sql.expression import true
from app.db import db
from app.models.coleccion import Coleccion
from app.helpers.auth import authenticated, check_permission

def index():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "index_collection"):
        abort(401)
    return render_template("colecciones/colecciones.html")

def create():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "create_collection"):
        abort(401)
    params=request.form
    nueva_coleccion=Coleccion(nombre=params["model_name"],descripcion=params["description"],fecha=params["fecha"],tipo=params["glasses_type"])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje="Se agrego la coleccion"
    flash(mensaje)
    return redirect(url_for("coleccion_index"))

def delete(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "destroy_collection"):
        abort(401)
    collection_to_delete = Coleccion.query.get_or_404(id)
    try:
        db.session.delete(collection_to_delete)
        db.session.commit()
        return redirect(url_for("coleccion_index"))
    except:
        return "Hubo un problema al borrar la coleccion"
from cgi import print_arguments
from flask import redirect, render_template, request, url_for, session, abort
import flask
from flask.helpers import flash
from sqlalchemy.sql.expression import true
#from app.resources.validadorColeccion import ValidarForm
from app.db import db
from app.models.coleccion import Coleccion

import requests
import json

def index():

    #Bonita Auth
    api_url = "http://localhost:8080/bonita/loginservice"
    headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"username": "walter.bates", "password": "bpm", "redirect": False}

    reqSession = requests.Session()

    response = reqSession.post(api_url, data=body, headers=headers)

    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    #Pegada crear proceso
    api_url = "http://localhost:8080/bonita/API/bpm/case"
    headers =  {"X-Bonita-API-Token": session["bonita_token"], "Content-Type":"application/json" }
    body = {"processDefinitionId": 5777042023671752656 }

    response = reqSession.post(api_url, data=body, headers=headers)

    print("aaaaaa", flush=True)
    print(response, flush=True)

    return render_template("colecciones/colecciones.html")

def collecion_create():
    params=request.form
    nueva_coleccion=Coleccion(nombre=params["model_name"],descripcion=params["description"],fecha=params["fecha"],tipo=params["glasses_type"])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje="Se agrego la coleccion"
    flash(mensaje)


    #Bonita auth
    reqSession = requests.Session()

    api_url = "http://localhost:8080/bonita/loginservice"
    headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"username": "walter.bates", "password": "bpm", "redirect": False}

    response = reqSession.post(api_url, data=body, headers=headers)

    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    #Pegada de crear tarea colleccion

    return redirect(url_for("home"))

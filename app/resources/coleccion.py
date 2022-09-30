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

    #reqSession queda cargada con las cookies de la respuesta del post
    reqSession.post(api_url, data=body, headers=headers)
    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    print("bonita token> " + session["bonita_token"], flush=True)
    print("bonita JSESSION> " + reqSession.cookies.get("JSESSIONID"), flush=True)

    #Pegada para traer el proceso Glasses para obtener su ID
    #"http://localhost:8080/bonita/API/bpm/process?f=name=Glasses&p=0&c=1&o=version%20desc&f=activationState=ENABLED"

    case_api_url = "http://localhost:8080/bonita/API/bpm/process?f=name=Glasses"
    case_headers = { 'Content/type' : 'application/json', 'X-Bonita-API-Token' : session["bonita_token"], 'JSESSIONID' : reqSession.cookies.get("JSESSIONID")}
    
    response = requests.get(case_api_url, headers=case_headers)

    print("aaa", flush=True)
    print(response.status_code, flush=True)
    print(response, flush=True)

    return render_template("colecciones/create_collection.html")

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

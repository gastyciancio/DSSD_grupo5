from flask import redirect, render_template, request, url_for, session
from flask.helpers import flash
from app.db import db
from app.models.coleccion import Coleccion

import requests

def index():

    #Bonita Auth
    api_url = "http://localhost:8080/bonita/loginservice"
    headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"username": "walter.bates", "password": "bpm", "redirect": False}

    reqSession = requests.Session()

    #reqSession queda cargada con las cookies de la respuesta del post
    reqSession.post(api_url, data=body, headers=headers)

    #Nos guardamos en la sesion la cookie con el token de bonita 
    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    #Pegada para traer el proceso Glasses para obtener su ID
    api_url = "http://localhost:8080/bonita/API/bpm/process?f=name=Glasses"
    process =  reqSession.get(api_url).json()[0]
    process_id = process["id"]
    print(process_id, flush=True)

    #-------------------------------------------------------------------------------------------

    #Bonita Auth
    api_url = "http://localhost:8080/bonita/loginservice"
    headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"username": "walter.bates", "password": "bpm", "redirect": False}

    reqSession.post(api_url, data=body, headers=headers)
    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    #Pegada para instanciar el proceso a partir del ID recuperado
    api_url = "http://localhost:8080/bonita/API/bpm/process/" + process_id + "/instantiation"
    headers = {"X-Bonita-API-Token": session["bonita_token"]}
    reqSession.post(api_url, headers=headers)
    



    #Aca configuramos las variables de bonita e iniciamos la primera tarea


    #Cargamos la vista del formulario
    return render_template("colecciones/create_collection.html")

def collecion_create():
    params=request.form
    nueva_coleccion=Coleccion(nombre=params["model_name"],descripcion=params["description"],fecha=params["fecha"],tipo=params["glasses_type"])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje="Se agrego la coleccion"
    flash(mensaje)

    #Bonita auth
    api_url = "http://localhost:8080/bonita/loginservice"
    headers =  {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"username": "walter.bates", "password": "bpm", "redirect": False}

    reqSession = requests.Session()

    #reqSession queda cargada con las cookies de la respuesta del post
    reqSession.post(api_url, data=body, headers=headers)

    # Nos guardamos en la sesion la cookie con el token de bonita 
    session["bonita_token"] = reqSession.cookies.get("X-Bonita-API-Token")

    #Pegada de crear tarea colleccion



    # Volvemos a la pantalla de inicio
    return redirect(url_for("home"))

from flask import redirect, render_template, request, url_for, session, Response
from flask.helpers import flash
from app.db import db
from app.models.coleccion import Coleccion
from app.models.image import Image


import requests
import json

def index():

    start_bonita_process()

    #Cargamos la vista del formulario
    return render_template('colecciones/create_collection.html')

def collecion_create():
    params=request.form
    if (params['model_name'] == '' or params['model_name'] == None):
        mensaje='Falta el nombre de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html")
    if (params['fecha'] == '' or params['fecha'] == None):
        mensaje='Falta la fecha de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html")
    
    nueva_coleccion=Coleccion(nombre=params['model_name'],descripcion=params['description'],fecha=params['fecha'],tipo=params['glasses_type'])
    db.session.add(nueva_coleccion)
    db.session.commit()
    mensaje='Se agrego la coleccion'
    flash(mensaje)
    
    set_collection_id_bonita_variable(nueva_coleccion.id)

    # Crear imagenes y agregarlas a esa coleccion
    imgs = request.files.getlist('images')
    
    if(len(imgs) == 1 and imgs[0].filename == ''):
        print("No se agregaron imagenes", flush=True)
    else:
        Image.save_images(imgs, nueva_coleccion.id)


    return render_template("/colecciones/create_collection.html")
    
    #return redirect(url_for('home'))
    #i=Image.query.filter_by(id=33).first()
    #return Response(i.img, mimetype=i.mimetype)


def start_bonita_process():

    #Bonita Auth
    api_url = 'http://localhost:8080/bonita/loginservice'
    headers =  {'Content-Type':'application/x-www-form-urlencoded'}
    body = {'username': 'walter.bates', 'password': 'bpm', 'redirect': False}

    reqSession = requests.Session()

    #reqSession queda cargada con las cookies de la respuesta del post
    reqSession.post(api_url, data=body, headers=headers)

    #Nos guardamos en la sesion la cookie con el token de bonita 
    session['X-Bonita-API-Token'] = reqSession.cookies.get('X-Bonita-API-Token')

    #Pegada para traer el proceso Glasses para obtener su ID
    api_url = 'http://localhost:8080/bonita/API/bpm/process?f=name=Glasses'
    process =  reqSession.get(api_url).json()[0]
    process_id = process['id']

    #-------------------------------------------------------------------------------------------

    #Pegada para instanciar el proceso a partir del ID recuperado
    api_url = "http://localhost:8080/bonita/API/bpm/case"
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
    variables = [{'name': 'collection_id', 'value':'' }]
    body = {
        "processDefinitionId":process_id,
        "variables": variables
    }
    body = json.dumps(body)
    case_id =  reqSession.post(api_url, data=body, headers=headers).json()['id']
    session['case_id'] = case_id

def set_collection_id_bonita_variable(collection_id):
    #Bonita Auth
    api_url = 'http://localhost:8080/bonita/loginservice'
    headers =  {'Content-Type':'application/x-www-form-urlencoded'}
    body = {'username': 'walter.bates', 'password': 'bpm', 'redirect': False}

    reqSession = requests.Session()

    #reqSession queda cargada con las cookies de la respuesta del post
    reqSession.post(api_url, data=body, headers=headers)

    #Nos guardamos en la sesion la cookie con el token de bonita 
    session['X-Bonita-API-Token'] = reqSession.cookies.get('X-Bonita-API-Token')

    #Recuperamos el case_id guarado en la sesion
    case_id = session['case_id']

    #Pegada para guardar el id de la coleccion en una variable de bonita
    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable/" + str(case_id) + "/collection_id"
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
    body = { 'type':'java.lang.String', 'value':str(collection_id) }
    body = json.dumps(body)
    variable =  reqSession.put(api_url, data=body, headers=headers)
    print(variable.status_code, flush=True)
    
    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable?f=case_id=" + str(case_id)
    print(reqSession.get(api_url, headers=headers).json(), flush=True)

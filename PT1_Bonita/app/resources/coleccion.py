from flask import redirect, render_template, request, url_for, session, Response
from flask.helpers import flash
from app.helpers.bonita_api import instantiate_process, set_case_variable
from app.models.coleccion import Coleccion
from app.models.image import Image

def index():

    instantiate_process()

    #Cargamos la vista del formulario
    return render_template('colecciones/create_collection.html')

def collecion_create():
    params = request.form
    if (params['model_name'] == '' or params['model_name'] == None):
        mensaje='Falta el nombre de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html")
    if (params['fecha'] == '' or params['fecha'] == None):
        mensaje='Falta la fecha de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html")
    
    nueva_coleccion = Coleccion.save_collection(params)
    mensaje='Se agrego la coleccion'
    flash(mensaje)
    
    set_case_variable("/collection_id", nueva_coleccion.id)

    # Crear imagenes y agregarlas a esa coleccion
    imgs = request.files.getlist('images')
    
    if(len(imgs) == 1 and imgs[0].filename == ''):
        print("No se agregaron imagenes a la coleccion creada", flush=True)
    else:
        Image.save_images(imgs, nueva_coleccion.id)

    # Crear los modelos y agregarlos a esa coleccion
    # ...
    #

    return render_template("/colecciones/create_collection.html")
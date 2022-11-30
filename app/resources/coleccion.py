from flask import redirect, render_template, request, url_for, session, Response
from flask.helpers import flash
from app.helpers.bonita_api import instantiate_process, set_case_variable, execute_next_task, get_cases_ids_of_collections_in_task
from app.models.coleccion import Coleccion
from app.models.model import Model
from app.models.material import Material
from app.models.image import Image
import json

def index():

    case_id=instantiate_process()

    get_cases_ids_of_collections_in_task(name="Planificar colección, fecha y plazos")
    #Cargamos la vista del formulario
    return render_template('colecciones/create_collection.html', case_id=case_id)


def collecion_create():
    params = request.form

    if (params['model_name'] == '' or params['model_name'] == None):
        mensaje='Falta el nombre de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html", case_id=params['case_id'])
    if (params['fecha'] == '' or params['fecha'] == None):
        mensaje='Falta la fecha de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/create_collection.html", case_id=params['case_id'])
    
    #validar los modelos
    counter = 0
    result = list(filter(lambda key: key.endswith(str(counter)), params.keys()))
    if (len(result) != 3):
            mensaje='Debe incluir al menos un modelo a la colección'
            flash(mensaje)
            return render_template("/colecciones/create_collection.html", case_id=params['case_id'])

    while (len(result) != 0):
        if (len(result) != 3 or len(list(filter(lambda key: params[key] == "", result))) > 0):
            mensaje='Se deben completar todos los campos de los modelos a incluir'
            flash(mensaje)
            return render_template("/colecciones/create_collection.html", case_id=params['case_id'])
        counter = counter + 1
        result = list(filter(lambda key: key.endswith(str(counter)), params.keys()))

    nueva_coleccion = Coleccion.save_collection(params)
    mensaje='Se agrego la coleccion'
    flash(mensaje)
    
    set_case_variable("/collection_id", nueva_coleccion.id, nueva_coleccion.case_id)
    set_case_variable("/collection_creator", session['username'], nueva_coleccion.case_id)

    # Crear imagenes y agregarlas a esa coleccion
    imgs = request.files.getlist('images')
    
    if(len(imgs) == 1 and imgs[0].filename == ''):
        print("No se agregaron imágenes a la colección creada", flush=True)
    else:
        Image.save_images(imgs, nueva_coleccion.id)

    # Crear los modelos y agregarlos a esa coleccion
    counter = 0
    result = list(filter(lambda key: key.endswith(str(counter)), params.keys()))
    
    while (len(result) != 0):     
        Model.save_model(params, result, nueva_coleccion.id)
        counter = counter + 1
        result = list(filter(lambda key: key.endswith(str(counter)), params.keys()))

    execute_next_task(case_id_collection=nueva_coleccion.case_id, name="Planificar colección, fecha y plazos")

    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Establecer materiales y cantidad necesarios")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)
    return render_template("/home.html", cols=collections)

def set_materials_and_quantities_index():
    #agarro el id de la coleccion seleccionada a la que se le van a establecer materiales
    collection_id = int(request.args.get('id_collection'))

    #agarro el objeto coleccion de la seleccionada
    selected_collection = Coleccion.findCollectionById(collection_id)
    return render_template("/colecciones/set_materials_and_quantities.html", col=selected_collection)

def set_materials_and_quantities():    
    params = request.form    

    form_status = "" 
    if(params['decition'] == "no"):
        form_status = "rechazado"
    else:
        form_status = "aceptado"
    
    id_collection = params['collectionId']
    selected_collection = Coleccion.findCollectionById(id_collection)
    set_case_variable("/establish_materials_form_status", form_status, selected_collection.case_id)

    execute_next_task(case_id_collection=selected_collection.case_id, name="Establecer materiales y cantidad necesarios")
    

    if(params['decition'] == "no"):
        print(params, flush=True)
        case_id_collections_active = get_cases_ids_of_collections_in_task(name="Establecer materiales y cantidad necesarios")
        collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

        return render_template("home.html", cols=collections)
    else:
        glass = params['vidrio']
        wood = params['madera']
        plastic = params['plastico']
        polycarbonate = params['policarbonato']        

        if (glass == "" or wood == "" or plastic == "" or polycarbonate == ""):
            mensaje='Los valores deben ser numéricos'
            flash(mensaje)
            return render_template("/colecciones/set_materials_and_quantities.html", col=selected_collection)

        glass = int(glass)
        wood = int(wood)
        plastic = int(plastic)
        polycarbonate = int(polycarbonate)
        
        if(glass < 0 or wood < 0 or plastic < 0 or polycarbonate < 0):
            mensaje='Los valores deben ser mayor o igual a 0'
            flash(mensaje)
            return render_template("/colecciones/set_materials_and_quantities.html", col=selected_collection)

        if (glass != 0):
            Material.save_material("vidrio", glass, id_collection)
        if (wood != 0):
            Material.save_material("madera", wood, id_collection)
        if (plastic != 0):
            Material.save_material("plastico", plastic, id_collection)
        if (polycarbonate != 0):
            Material.save_material("policarbonato", polycarbonate, id_collection)

        session['id_coleccion_materials'] = id_collection

        return redirect(url_for("providers_form"))

def colecctions_ready():
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Lanzar la colección y distribuir")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

    return render_template("/colecciones/colecciones_ready.html", cols=collections)

def lanzar(case_id):
    execute_next_task(case_id_collection=case_id, name="Lanzar la colección y distribuir")
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Lanzar la colección y distribuir")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)
    return render_template("/colecciones/colecciones_ready.html", col=collections)

def update_index():
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Planificar colección, fecha y plazos")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)
    return render_template("/colecciones/update_collection_index.html", cols=collections)

def update(id):
    coleccion= Coleccion.findCollectionById(id)
   
    print("id de la coleccion a updetear", id, flush=True)
    params = request.form
    
    if (params['model_name'] == '' or params['model_name'] == None):
        mensaje='Falta el nombre de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/update_collection_index.html", col=coleccion)
    if (params['fecha'] == '' or params['fecha'] == None):
        mensaje='Falta la fecha de la coleccion'
        flash(mensaje)
        return render_template("/colecciones/update_collection_index.html", col=coleccion)

    update_coleccion = Coleccion.update_collection(params,id)
    mensaje='Se actualizó la colección'
    flash(mensaje)
    
    set_case_variable("/collection_creator", session['username'], coleccion.case_id)

    # Crear imagenes y agregarlas a esa coleccion
    #imgs = request.files.getlist('images')
    #
    #if(len(imgs) == 1 and imgs[0].filename == ''):
    #    print("No se agregaron imágenes a la colección creada", flush=True)
    #else:
    #    Image.delete_images(update_coleccion.id)
    #    Image.save_images(imgs, update_coleccion.id)

    execute_next_task(case_id_collection=coleccion.case_id, name="Planificar colección, fecha y plazos")

    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Establecer materiales y cantidad necesarios")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

    return render_template("home.html", cols=collections)
   

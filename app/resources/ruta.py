from flask import render_template, request
from flask.helpers import flash
from app.models.ruta import Ruta
from app.models.coleccion import Coleccion
from app.helpers.bonita_api import set_case_variable, execute_next_task, get_cases_ids_of_collections_in_task, get_case_variable_value

def index():
    current_collection_id = request.args['current_collection_id']

    return render_template('rutas/create_ruta.html', col_id=current_collection_id)

def ruta_create():

    current_collection_id = request.form['col_id']
    case_id = Coleccion.findCollectionById(current_collection_id).case_id

    params = request.form
    if (params['ruta'] == ''):
        mensaje='Falta especificar la ruta'
        flash(mensaje)
        return render_template("/rutas/create_ruta.html", col_id=current_collection_id)
    rutas_extras = request.form.getlist("ruta_extra")
    id_coleccion = get_case_variable_value("/collection_id", case_id)
    if (id_coleccion != None):
        id_coleccion = int(id_coleccion)
        Ruta.save_ruta(params['ruta'],id_coleccion)
        for ruta_extra in rutas_extras:
            if (ruta_extra != ''):
                Ruta.save_ruta(ruta_extra,id_coleccion)
        mensaje='Se agrego la/s ruta/s'
        flash(mensaje)

        #SETEO PARA ELEGIR UN RUMBO DE FLUJO FINAL
        set_case_variable("/cambio_pedido", 'no', case_id)
        set_case_variable("/quedan_proveedores", 'no', case_id)
        set_case_variable("/seguir_curso_normal", 'si', case_id)
        execute_next_task(case_id_collection=case_id, name="Establecer las rutas involucradas")
        
        return render_template("/rutas/create_ruta.html", col_id=current_collection_id)
    else:
        flash('No se pudo obtener el id de la coleccion a traves de bonita')
        return render_template("/rutas/create_ruta.html", col_id=current_collection_id)

def list_collections_in_task_select_routes():
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Establecer las rutas involucradas")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

    return render_template("/rutas/collections_in_task_select_routes.html", cols=collections)
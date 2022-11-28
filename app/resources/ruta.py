from flask import render_template, request
from flask.helpers import flash
from app.models.ruta import Ruta
from app.helpers.bonita_api import get_case_variable_value
from app.helpers.bonita_api import set_case_variable, execute_next_task

def index():
    #Cargamos la vista del formulario
    return render_template('rutas/create_ruta.html')

def ruta_create():
    params = request.form
    if (params['ruta'] == ''):
        mensaje='Falta especificar la ruta'
        flash(mensaje)
        return render_template("/rutas/create_ruta.html")
    rutas_extras = request.form.getlist("ruta_extra")
    id_coleccion = get_case_variable_value("/collection_id")
    if (id_coleccion != None):
        id_coleccion = int(id_coleccion)
        Ruta.save_ruta(params['ruta'],id_coleccion)
        for ruta_extra in rutas_extras:
            if (ruta_extra != ''):
                Ruta.save_ruta(ruta_extra,id_coleccion)
        mensaje='Se agrego la/s ruta/s'
        flash(mensaje)

        #SETEO PARA ELEGIR UN RUMBO DE FLUJO FINAL
        set_case_variable("/cambio_pedido", 'no')
        set_case_variable("/quedan_proveedores", 'no')
        set_case_variable("/seguir_curso_normal", 'si')
        execute_next_task(name="Establecer las rutas involucradas")
        
        return render_template("/rutas/create_ruta.html")
    else:
        flash('No se pudo obtener el id de la coleccion a traves de bonita')
        return render_template("/rutas/create_ruta.html")

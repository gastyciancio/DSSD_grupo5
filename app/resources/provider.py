from flask import render_template, request,redirect,url_for, session
from flask.helpers import flash
import re
from app.models.coleccion import Coleccion
from app.models.material import Material
from app.helpers.bonita_api import set_case_variable, execute_next_task, get_cases_ids_of_collections_in_task
import datetime

from app.helpers.providers_maker_api import get_providers_by_data, reserve_providers_by_data, get_providers_with_only_materials

def index():
    current_collection_id = request.args['current_collection_id']

    #id_collection = session['id_coleccion_materials']
    current_coleccion = Coleccion.findCollectionById(current_collection_id)
    materiales_bd = Material.get_material()
    materiales_of_collection = []
    for material in materiales_bd:
        if (material.coleccion_id == int(current_collection_id)):
            materiales_of_collection.append(material)
    
    materiales_for_api = []

    for material in materiales_of_collection:
        materiales_for_api.append({
            "name":             material.name,
            "amount":           material.amount,
            "date_required":    datetime.datetime.strptime(current_coleccion.fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
        })

    response = get_providers_with_only_materials(materiales_for_api)
    print(response)
    materiales_sin_prov = response['metadata']['materiales_sin_proveedor']
    materiales_con_prov = response['suppliers']
    session['materiales_con_prov'] = materiales_con_prov
    session['materiales_sin_prov'] = response['metadata']['materiales_sin_proveedor']

    materiales_pedidos = materiales_for_api

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_prov:
            for material_prov in supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']

    return render_template('providers/reserve_providers.html',materiales_con_prov=materiales_con_prov, materiales_sin_prov=materiales_sin_prov, col_id = current_collection_id)

def search():
    current_collection_id = request.form['col_id']
    current_collection = Coleccion.findCollectionById(current_collection_id)

    set_case_variable("/more_providers", 'si', current_collection.case_id)
    
    materiales_bd = Material.get_material()
    materiales_of_collection = []
    for material in materiales_bd:
        if (material.coleccion_id == int(current_collection_id)):
            materiales_of_collection.append(material)
    
    materiales_for_api = []

    for material in materiales_of_collection:
        materiales_for_api.append({
            "name":             material.name,
            "amount":           material.amount,
            "date_required":    datetime.datetime.strptime(current_collection.fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
        })
    response = get_providers_by_data(request.form, materiales_for_api)
    print(response)
    materiales_sin_prov = response['metadata']['materiales_sin_proveedor']
    materiales_con_prov = response['suppliers']
    session['materiales_con_prov'] = materiales_con_prov
    session['materiales_sin_prov'] = response['metadata']['materiales_sin_proveedor']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANTIDADES ESTABLECIDOS
    materiales_pedidos = materiales_for_api

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_prov:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']
    
    execute_next_task(case_id_collection=current_collection.case_id, name="Seleccionar los proveedores")

    return render_template('providers/reserve_providers.html',materiales_con_prov=materiales_con_prov, materiales_sin_prov=materiales_sin_prov, col_id = current_collection_id)


def reserve():
    current_collection_id = request.form['col_id']
    case_id = Coleccion.findCollectionById(current_collection_id).case_id

    provedores_elegidos = request.form.getlist("seleccionar_proveedor")
    valores = []
    for proveedor in provedores_elegidos:
        prov = re.findall(r'\d+',proveedor)
        prov = [int(num) for num in prov]
        valores.append(prov)
    valores = sorted(valores)
    suppliers = []

    if (len(valores) == 0):
        flash('Debe elegir proveedores antes de reservar')
        return redirect(url_for("providers_form", current_collection_id=current_collection_id)) 

    i=0
    valor_antiguo= valores[i][0]
    while (i<len(valores)):
        materiales = []
        while (i<len(valores) and valores[i][0] == valor_antiguo):
            materiales.append(
                {
                    "id": valores[i][1],
                    "amount": valores[i][2]
                }
            )
            valor_antiguo = valores[i][0]
            i = i + 1
        suppliers.append(
            { 
                "id": valor_antiguo,
                "materials": materiales
            }
        )
        if (i<len(valores)):
            valor_antiguo = valores[i][0]
        


    body = {"suppliers": suppliers}
    response = reserve_providers_by_data(body)
    if (response !=None):
        for message in response['response']:
            flash(message)
        set_case_variable("/more_providers", 'no', case_id)
        execute_next_task(case_id_collection=case_id, name="Seleccionar los proveedores")
        case_id_collections_active = get_cases_ids_of_collections_in_task(name="Seleccionar los proveedores")
        collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

        return render_template("/providers/collections_in_task_select_providers.html", cols=collections)
    else:
        flash('Fallo la reserva de proveedores')
        return redirect(url_for("providers_form", current_collection_id=current_collection_id))

def list_collections_in_task_select_providers():
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Seleccionar los proveedores")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

    return render_template("/providers/collections_in_task_select_providers.html", cols=collections)


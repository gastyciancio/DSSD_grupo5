from flask import render_template, request,redirect,url_for, session
from flask.helpers import flash
import re
from app.models.coleccion import Coleccion
from app.models.material import Material
from app.helpers.bonita_api import set_case_variable, execute_next_task, get_cases_ids_of_collections_in_task
import datetime

from app.helpers.providers_maker_api import get_maker_with_only_materials,get_makers_by_data,reserve_makers_by_data

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
            "amount":           material.amount
        })

    fecha = datetime.datetime.strptime(current_coleccion.fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
    response = get_maker_with_only_materials(materiales_for_api,fecha)
    print(response)
    materiales_sin_fabri = response['metadata']['materiales_sin_fabricante']
    materiales_con_fabri = response['makers']
    session['materiales_con_fabri'] = materiales_con_fabri
    session['materiales_sin_fabri'] = response['metadata']['materiales_sin_fabricante']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANT ESTABLECIDOS
    materiales_pedidos = materiales_for_api

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_fabri:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']
    

    return render_template('makers/reserve_makers.html',materiales_con_fabri=materiales_con_fabri, materiales_sin_fabri=materiales_sin_fabri, col_id=current_collection_id)

def search():
    current_collection_id = request.form['col_id']
    current_collection = Coleccion.findCollectionById(current_collection_id)

    set_case_variable("/more_makers", 'si', current_collection.case_id)        
    
    materiales_bd = Material.get_material()
    materiales_of_collection = []
    for material in materiales_bd:
        if (material.coleccion_id == int(current_collection_id)):
            materiales_of_collection.append(material)
    
    materiales_for_api = []

    for material in materiales_of_collection:
        materiales_for_api.append({
            "name":             material.name,
            "amount":           material.amount
        })

    fecha = datetime.datetime.strptime(current_collection.fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
    response = get_makers_by_data(request.form, materiales_for_api, fecha)
    print(response)
    materiales_sin_fabri = response['metadata']['materiales_sin_fabricante']
    materiales_con_fabri = response['makers']
    session['materiales_con_fabri'] = materiales_con_fabri
    session['materiales_sin_fabri'] = response['metadata']['materiales_sin_fabricante']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANTIDADES ESTABLECIDOS
    materiales_pedidos = materiales_for_api

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_fabri:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']

    execute_next_task(case_id_collection=current_collection.case_id, name="Seleccionar los fabricantes")
    return render_template('makers/reserve_makers.html',materiales_con_fabri=materiales_con_fabri, materiales_sin_fabri=materiales_sin_fabri, col_id=current_collection_id)


def reserve():
    current_collection_id = request.form['col_id']
    case_id = Coleccion.findCollectionById(current_collection_id).case_id

    fabricantes_elegidos = request.form.getlist("seleccionar_fabricante")
    valores = []
    for fabricante in fabricantes_elegidos:
        fabri = re.findall(r'\d+',fabricante)
        fabri = [int(num) for num in fabri]
        valores.append(fabri)
    valores = sorted(valores)
    makers = []

    if (len(valores) == 0):
        flash('Debe elegir fabricantes antes de reservar')
        return redirect(url_for("makers_form", current_collection_id=current_collection_id)) 

    i=0
    valor_antiguo= valores[i][0]
    fecha_antigua= str(valores[i][3])+"/"+str(valores[i][4])+"/"+str(valores[i][5])
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
            fecha_antigua= str(valores[i][3])+"/"+str(valores[i][4])+"/"+str(valores[i][5])
            i = i + 1
        # CAMBIAR AMOUNT GLASSES, ESE VALOR SE ESTABLECE ANTES
        makers.append(
            { 
                "id": valor_antiguo,
                "materials": materiales,
                "date_deliver":fecha_antigua,
                "amount_glasses": 10

            }
        )
        if (i<len(valores)):
            valor_antiguo = valores[i][0]
            fecha_antigua= str(valores[i][3])+"/"+str(valores[i][4])+"/"+str(valores[i][5])

    body = {"makers": makers}
    response = reserve_makers_by_data(body)
    if (response !=None):
        for message in response['response']:
            flash(message)
        set_case_variable("/more_makers", 'no', case_id)
        execute_next_task(case_id_collection=case_id, name="Seleccionar los fabricantes")
        return redirect(url_for("rutas_form", current_collection_id=current_collection_id))
    else:
        flash('Fallo la reserva de fabricantes')
        return redirect(url_for("makers_form", current_collection_id=current_collection_id))

def list_collections_in_task_select_makers():
    case_id_collections_active = get_cases_ids_of_collections_in_task(name="Seleccionar los fabricantes")
    collections = Coleccion.findCollectionByCaseId(case_id_collections_active)

    return render_template("/makers/collections_in_task_select_makers.html", cols=collections)

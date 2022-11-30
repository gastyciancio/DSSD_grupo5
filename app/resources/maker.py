from flask import render_template, request,redirect,url_for, session
from flask.helpers import flash
import re
from app.models.coleccion import Coleccion
from app.models.material import Material
from app.helpers.bonita_api import set_case_variable, execute_next_task
import datetime

from app.helpers.providers_maker_api import get_maker_with_only_materials,get_makers_by_data,reserve_makers_by_data

def index():

    id_collection = session['id_coleccion_materials']
    current_coleccion = Coleccion.findCollectionById(id_collection)
    materiales_bd = Material.get_material()
    materiales_of_collection = []
    for material in materiales_bd:
        if (material.coleccion_id == int(id_collection)):
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
    

    return render_template('makers/reserve_makers.html',materiales_con_fabri=materiales_con_fabri, materiales_sin_fabri=materiales_sin_fabri)

def search():
    id_collection = session['id_coleccion_materials']
    current_coleccion = Coleccion.findCollectionById(id_collection)

    set_case_variable("/more_makers", 'si', current_coleccion.case_id)        
    
    materiales_bd = Material.get_material()
    materiales_of_collection = []
    for material in materiales_bd:
        if (material.coleccion_id == int(id_collection)):
            materiales_of_collection.append(material)
    
    materiales_for_api = []

    for material in materiales_of_collection:
        materiales_for_api.append({
            "name":             material.name,
            "amount":           material.amount
        })

    fecha = datetime.datetime.strptime(current_coleccion.fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
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

    execute_next_task(case_id_collection=current_coleccion.case_id, name="Seleccionar los fabricantes")
    return render_template('makers/reserve_makers.html',materiales_con_fabri=materiales_con_fabri, materiales_sin_fabri=materiales_sin_fabri)


def reserve():
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
        return redirect(url_for("makers_form")) 

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
    proveedores_reservados = 0
    if (response !=None):
        for message in response['response']:
            flash(message) 
            if (message['message'] == 'El fabricante reservo el espacio'):
                proveedores_reservados = proveedores_reservados + 1
        set_case_variable("/more_makers", 'no')
        set_case_variable("/contador_proveedores", int(proveedores_reservados), type ='Integer')
        execute_next_task(name="Seleccionar los fabricantes")
        return redirect(url_for("rutas_form"))
    else:
        flash('Fallo la reserva de fabricantes')
        return redirect(url_for("makers_form"))
from flask import render_template, request,redirect,url_for, session
from flask.helpers import flash
import re

from app.helpers.providers_maker_api import get_providers_by_data, reserve_providers_by_data, get_providers_with_only_materials

def index():
    response = get_providers_with_only_materials()
    print(response)
    materiales_sin_prov = response['metadata']['materiales_sin_proveedor']
    materiales_con_prov = response['suppliers']
    session['materiales_con_prov'] = materiales_con_prov
    session['materiales_sin_prov'] = response['metadata']['materiales_sin_proveedor']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANT ESTABLECIDOS
    materiales_pedidos = [  
                    {
                        "name": "Madera",
                        "amount": 1,
                        "date_required": "17/11/2022"
                    },
                    {
                        "name": "Vidrio",
                        "amount": 1,
                        "date_required": "18/11/2022"
                    }
                ]

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_prov:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']
    

    return render_template('providers/reserve_providers.html',materiales_con_prov=materiales_con_prov, materiales_sin_prov=materiales_sin_prov)

def search():
    response = get_providers_by_data(request.form)
    print(response)
    materiales_sin_prov = response['metadata']['materiales_sin_proveedor']
    materiales_con_prov = response['suppliers']
    session['materiales_con_prov'] = materiales_con_prov
    session['materiales_sin_prov'] = response['metadata']['materiales_sin_proveedor']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANTIDADES ESTABLECIDOS
    materiales_pedidos = [  
            {
                "name": "Madera",
                "amount": 1,
                "date_required": "17/11/2022"
            },
            {
                "name": "Vidrio",
                "amount": 1,
                "date_required": "18/11/2022"
            }
        ]

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_prov:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']

    return render_template('providers/reserve_providers.html',materiales_con_prov=materiales_con_prov, materiales_sin_prov=materiales_sin_prov)


def reserve():
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
        return redirect(url_for("providers_form")) 

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
    else:
        flash('Fallo la reserva')
    return redirect(url_for("providers_form"))
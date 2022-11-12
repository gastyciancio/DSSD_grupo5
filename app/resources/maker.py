from flask import render_template, request,redirect,url_for, session
from flask.helpers import flash
import re

from app.helpers.providers_maker_api import get_maker_with_only_materials,get_makers_by_data,reserve_makers_by_data

def index():
    response = get_maker_with_only_materials()
    print(response)
    materiales_sin_fabri = response['metadata']['materiales_sin_fabricante']
    materiales_con_fabri = response['makers']
    session['materiales_con_fabri'] = materiales_con_fabri
    session['materiales_sin_fabri'] = response['metadata']['materiales_sin_fabricante']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANT ESTABLECIDOS
    materiales_pedidos = [  
                    {
                        "name": "Madera",
                        "amount": 4
                    },
                    {
                        "name": "Vidrio",
                        "amount": 7
                    },
                    {
                        "name": "piso",
                        "amount": 7
                    }
                ]

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_fabri:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']
    

    return render_template('makers/reserve_makers.html',materiales_con_fabri=materiales_con_fabri, materiales_sin_fabri=materiales_sin_fabri)

def search():
    response = get_makers_by_data(request.form)
    print(response)
    materiales_sin_fabri = response['metadata']['materiales_sin_fabricante']
    materiales_con_fabri = response['makers']
    session['materiales_con_fabri'] = materiales_con_fabri
    session['materiales_sin_fabri'] = response['metadata']['materiales_sin_fabricante']

    #CAMBIAR CUANDO TENGAMOS LOS MATERIALES Y SUS CANTIDADES ESTABLECIDOS
    materiales_pedidos = [  
                    {
                        "name": "Madera",
                        "amount": 4
                    },
                    {
                        "name": "Vidrio",
                        "amount": 7
                    },
                    {
                        "name": "piso",
                        "amount": 7
                    }
                ]

    for material in materiales_pedidos:
        for supplier_with_materials in materiales_con_fabri:
            for material_prov in  supplier_with_materials['materials']:
                if material_prov['name'].lower() == material['name'].lower():
                    material_prov['amount'] = material['amount']

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
    if (response !=None):
        for message in response['response']:
            flash(message)
    else:
        flash('Fallo la reserva de fabricantes')
    return redirect(url_for("makers_form"))
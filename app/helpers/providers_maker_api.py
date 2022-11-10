from flask import session
import requests, json

#Login
def providers_makers_auth():
    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/auth/'
    body = {'username': 'walter.bates', 'password': 'admin123'}

    #reqSession queda cargada con las cookies de la respuesta del post
    res = reqSession.post(api_url, data=json.dumps(body))
 
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en el login a la api de proveedores/fabricantes", flush=True)
    else:
        session['token_providers'] = res.json()['access_token']
        print("login api proveedores/fabricantes exitoso", flush=True)
    
    return res

def get_providers_by_data(params):

    providers_makers_auth()

    filtro_precio = params['filtro_precio']
    dias_extra = params['dias_extra']
    #materiales = params['materiales']

   
    #materiales_to_api = []
    #for material in materiales:
    #    materiales_to_api.append({"name": material["name"],"amount": material["amount"],"date_required": material["date_required"]})

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/suppliers/by_data'
    body = { "materiales":[  
                    {
                        "name": "Madera",
                        "amount": 15,
                        "date_required": "17/11/2022"
                    },
                    {
                        "name": "Terracota",
                        "amount": 15,
                        "date_required": "17/11/2022"
                    }
                ]
            }

    if (params['filtro_precio'] != '' or params['filtro_precio'] != None):
        body['filtro_precio'] = int(filtro_precio)
    if (params['dias_extra'] != '' or params['dias_extra'] != None):
        body['dias_extra'] = int(dias_extra)

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    proveedores = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo obtener proveedores by data", flush=True)
    else:
        proveedores = res.json()
    return proveedores

def reserve_providers_by_data(data):
    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/suppliers/reserve'
    body = {
            "suppliers": [
                {
                "id": 1,
                "materials": [
                    {
                    "id": 2,
                    "amount": 1
                    }
                ]
                },
                {
                "id": 2,
                "materials": [
                    {
                    "id": 1,
                    "amount": 1
                    }
                ]
                }
            ]
            }

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    breakpoint()

    res = reqSession.post(api_url, data=json.dumps(body), headers=headers)
    response = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo reserva de proveedores by data", flush=True)
    else:
        response = res.json()
    breakpoint()
    return response
    
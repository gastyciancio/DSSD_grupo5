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

def get_providers_with_only_materials():
    
    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/suppliers/by_data'

    #CAMBIAR POR MATERIALES QUE POSTA SE NECESITAN
    body = { "materiales":[  
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
            }

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    proveedores = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo obtener proveedores by data", flush=True)
    else:
        proveedores = res.json()
    return proveedores


def get_providers_by_data(params):

    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/suppliers/by_data'

    #CAMBIAR POR MATERIALES QUE POSTA SE NECESITAN
    body = { "materiales":[  
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
            }
    if (params['filtro_precio'] != '' and params['filtro_precio'] != None):
        body['filtro_precio'] = int(params['filtro_precio'])
    if (params['dias_extra'] != '' and params['dias_extra'] != None):
        body['dias_extra'] = int(params['dias_extra'])

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    proveedores = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo obtener proveedores by data", flush=True)
    else:
        proveedores = res.json()
    return proveedores

def reserve_providers_by_data(body):
    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/suppliers/reserve'

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    response = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo reserva de proveedores by data", flush=True)
    else:
        response = res.json()
    return response
    
def get_maker_with_only_materials():
    
    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/makers/by_data'

    #CAMBIAR POR MATERIALES QUE POSTA SE NECESITAN
    body = { "materiales":[  
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
                ],
                "date_deliver":"20/12/2022",
                "amount_glasses":10
            }

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    fabricantes = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo obtener fabricantes by data", flush=True)
    else:
        fabricantes = res.json()
    return fabricantes


def get_makers_by_data(params):

    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/makers/by_data'

    #CAMBIAR POR MATERIALES QUE POSTA SE NECESITAN
    body = { "materiales":[  
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
                ],
                "date_deliver":"20/12/2022",
                "amount_glasses":10
            }

    if (params['filtro_precio'] != '' and params['filtro_precio'] != None):
        body['filtro_precio'] = int(params['filtro_precio'])
    if (params['dias_extra'] != '' and params['dias_extra'] != None):
        body['dias_extra'] = int(params['dias_extra'])

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    fabricantes = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo obtener fabricantes by data", flush=True)
    else:
        fabricantes = res.json()
    return fabricantes

def reserve_makers_by_data(body):
    providers_makers_auth()

    reqSession = requests.Session()

    api_url = 'https://apidssd.fly.dev/makers/reserve'

    headers =  {'Authorization': 'Bearer '+session['token_providers']}

    res = reqSession.post(api_url, json=body, headers=headers)
    response = None
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo reserva de fabricantes by data", flush=True)
    else:
        response = res.json()
    return response
    
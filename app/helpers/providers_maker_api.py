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

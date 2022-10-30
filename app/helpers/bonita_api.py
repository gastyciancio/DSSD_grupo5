from flask import session
import requests, json

#Login
def bonita_auth():
    reqSession = requests.Session()

    api_url = 'http://localhost:8080/bonita/loginservice'
    headers =  {'Content-Type':'application/x-www-form-urlencoded'}
    body = {'username': session['username'], 'password': session['password'], 'redirect': False}

    #reqSession queda cargada con las cookies de la respuesta del post
    res = reqSession.post(api_url, data=body, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en el login", flush=True)
    else:
        print("login exitoso", flush=True)
    
    #Nos guardamos en la sesion la cookie con el token de bonita 
    session['X-Bonita-API-Token'] = reqSession.cookies.get('X-Bonita-API-Token')

    return reqSession

#Traer el id del proceso Glasses
def get_process_id():

    reqSession = bonita_auth()

    api_url = 'http://localhost:8080/bonita/API/bpm/process?f=name=Glasses'
    res = reqSession.get(api_url)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en get process id", flush=True)
    else:
        print("get process id exitoso, id: " + res.json()[0]["id"], flush=True)
    
    return res.json()[0]["id"]

#Instanciar un proceso Glasses. Y tambien guarda su id en la sesion
def instantiate_process():
    
    process_id = get_process_id()
    reqSession = bonita_auth()

    api_url = "http://localhost:8080/bonita/API/bpm/case"
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
    variables = [{'name': 'collection_id', 'value':'' }]
    body = {
        "processDefinitionId":process_id,
        "variables": variables
    }
    body = json.dumps(body)

    res =  reqSession.post(api_url, data=body, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en instantiate process", flush=True)
    else:
        print("instantiate process id exitoso, id: " + res.json()['id'], flush=True)

    session['case_id'] = res.json()['id']

#Setea una variable en el case con id guardado en la sesion
#Si se hacen varios set, se hacen todos sobre el mismo case
def set_case_variable(var_name, var_value):
    
    reqSession = bonita_auth()
    case_id = session['case_id']

    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable/" + str(case_id) + var_name
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
    body = { 'type':'java.lang.String', 'value':str(var_value) }
    body = json.dumps(body)

    res = reqSession.put(api_url, data=body, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en set case variable", flush=True)
    else:
        print("set case variable exitoso", flush=True)
    
    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable?f=case_id=" + str(case_id)
    print(reqSession.get(api_url, headers=headers).json(), flush=True)
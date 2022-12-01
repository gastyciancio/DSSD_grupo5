from flask import session
import requests, json
from app.models.coleccion import Coleccion

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
    variables = [
        {'name': 'collection_id', 'value':'' },
        {'name': 'collection_creator', 'value':'' },
        {'name': 'establish_materials_form_status', 'value': ''},
        {'name': 'more_providers', 'value': ''},
        {'name': 'more_makers', 'value': ''},
        {'name': 'cambio_pedido', 'value': ''},
        {'name': 'quedan_proveedores', 'value': ''},
        {'name': 'seguir_curso_normal', 'value': ''} 
    ]
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
    return session['case_id']

#Setea una variable en el case con id guardado en la sesion
#Si se hacen varios set, se hacen todos sobre el mismo case
def set_case_variable(var_name, var_value, case_id_collection=None, type = 'String'):
    reqSession = bonita_auth()
    #SACAR IF
    if(case_id_collection == None):
        case_id = session['case_id']
    else:
        case_id = case_id_collection

    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable/" + str(case_id) + var_name
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
    body = { 'type':'java.lang.'+type, 'value':str(var_value) }
    body = json.dumps(body)

    res = reqSession.put(api_url, data=body, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en set case variable", flush=True)
    else:
        print("set case variable exitoso", flush=True)
    
    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable?f=case_id=" + str(case_id)
    print(reqSession.get(api_url, headers=headers).json(), flush=True)

#Setea una variable en el case con id guardado en la sesion
#Si se hacen varios set, se hacen todos sobre el mismo case
def get_case_variable_value(var_name, case_id_collection=None):
    reqSession = bonita_auth()
    #SACAR IF
    if(case_id_collection == None):
        case_id = session['case_id']
    else:
        case_id = case_id_collection

    api_url = "http://localhost:8080/bonita/API/bpm/caseVariable/" + str(case_id) + var_name
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}

    res = reqSession.get(api_url, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en get case variable", flush=True)
        return None
    else:
        print("get case variable exitoso", flush=True)
        return res.json()['value']

def current_user_id():
    
    reqSession = bonita_auth()
    api_url = 'http://localhost:8080/bonita/API/identity/user?p=0&c=10'
    users = (reqSession.get(api_url)).json()
    usuario_id = None
    for user in users:
        if (user['userName'] == session['username']):
            usuario_id = user['id']
            break
    return usuario_id
   

# EJEMPLO: execute_next_task('userTask','Planificar colección, fecha y plazos') SE PONE EL NOMBRE DE LA TAREA DONDE ESTAMOS PARADOS
def execute_next_task(case_id_collection=None, type_task='userTask', name='poner nombre de tarea'):
    reqSession = bonita_auth()
    #SACAR IF
    if(case_id_collection == None):
        case_id = session['case_id']
    else:
        case_id = case_id_collection

    api_url = "http://localhost:8080/bonita/API/bpm/" + str(type_task) +'?f=caseId='+str(case_id)+'&f=name='+name
    headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}

    res = reqSession.get(api_url, headers=headers)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en traer tarea", flush=True)
    else:
        print("Traer tarea exitosa", flush=True)
        tarea = res.json()[0]
        id_tarea = tarea['id']

        api_url = "http://localhost:8080/bonita/API/bpm/" + str(type_task) +'/'+id_tarea
        headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}
        body = {
            "assigned_id":current_user_id()
        }
        
        body = json.dumps(body) 
        res = reqSession.put(api_url, data=body, headers=headers)
        if(res.status_code < 200 or res.status_code > 299):
            print("Fallo asignar tarea", flush=True)
        else:
            print("Asignacion de tarea al usuario actual exitosa", flush=True)

            reqSession = bonita_auth()
            api_url = "http://localhost:8080/bonita/API/bpm/" + str(type_task) +'/'+id_tarea+'/execution'
            headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}

            res = reqSession.post(api_url, headers=headers)
            if(res.status_code < 200 or res.status_code > 299):
                print("Fallo en ejecutar siguiente tarea", flush=True)
            else:
                print("Ejecuto tarea exitosamente", flush=True)
                api_url = "http://localhost:8080/bonita/API/bpm/" + str(type_task) +'?f=caseId='+str(case_id)
                headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}

                res = reqSession.get(api_url, headers=headers)
                if(res.status_code < 200 or res.status_code > 299):
                    print("Fallo en traer tareas despues de ejecutar siguiente", flush=True)
                    return None
                else:
                    print("Traer tareas exitosa despues de ejecutar siguiente", flush=True)
                    return res.json()

def get_cases_ids_of_collections_in_task(type_task='userTask', name='poner nombre de tarea'):
    reqSession = bonita_auth()
    
    case_id_collections_active = []
    collections = Coleccion.getAll()
    for col in collections:
        api_url = "http://localhost:8080/bonita/API/bpm/" + str(type_task) +'?f=caseId='+str(col.case_id)+'&f=name='+name
        headers = {'X-Bonita-API-Token': session['X-Bonita-API-Token']}

        res = reqSession.get(api_url, headers=headers)
        if(res.status_code < 200 or res.status_code > 299):
            print("Fallo en traer tarea", flush=True)
        else:
            print("Traer tarea exitosa", flush=True)

        if len(res.json()) != 0:        
            case_id_collections_active.append(res.json()[0]['rootContainerId'])
        
    return case_id_collections_active

# Lista de nombres de los todos los usuarios con rol 'creativo'
def get_all_bonita_designer_usernames():
    reqSession = bonita_auth()
    api_url = 'http://localhost:8080/bonita/API/identity/user?p=0&c=10'
    users = (reqSession.get(api_url)).json()

    usernames = []

    for user in users:
        api_url = 'http://localhost:8080/bonita/API/identity/membership?f=user_id='+ str(user['id'])
        membresias = (reqSession.get(api_url)).json()
        for membresia in membresias:
            api_url = 'http://localhost:8080/bonita/API/identity/role/'+ membresia['role_id']
            rol = (reqSession.get(api_url)).json()
            if (rol['name'].lower() == 'creativo'):
                usernames.append(user['userName'])

    return usernames

def get_all_running_cases():
    reqSession = bonita_auth()
    process_id = get_process_id()

    api_url = 'http://localhost:8080/bonita/API/bpm/case?p=0&c=100&f=processDefinitionId=' + process_id
    res = reqSession.get(api_url)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en get all running cases", flush=True)
    else:
        print("get all running cases exitoso", flush=True)
    
    print(res.json(), flush=True)

    return res.json()

def get_all_archived_cases():
    reqSession = bonita_auth()
    process_id = get_process_id()

    api_url = 'http://localhost:8080/bonita/API/bpm/archivedCase?p=0&c=100&f=processDefinitionId=' + process_id
    res = reqSession.get(api_url)
    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en get all archived cases", flush=True)
    else:
        print("get all archived cases exitoso", flush=True)
    
    print(res.json(), flush=True)

    return res.json()
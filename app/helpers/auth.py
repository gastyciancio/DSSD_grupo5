from app.models.usuario import Usuario
from flask import session
from app.helpers.bonita_api import bonita_auth


def authenticated(session):
    return session.get("username")


def check_permission(user_id, permission):
    if(user_id!=0):
        return Usuario.has_permission(user_id,permission)
    else:
        return False

def check_permission_bonita(permission):
    if authenticated(session):
        reqSession = bonita_auth()
        api_url = 'http://localhost:8080/bonita/API/identity/user?p=0&c=10'
        users = (reqSession.get(api_url)).json()
        usuario_id = None
        for user in users:
            if (user['userName'] == session['username']):
                usuario_id = user['id']
                break
        if usuario_id == None:
            return False
        else:
            api_url = 'http://localhost:8080/bonita/API/identity/membership?f=user_id='+ str(usuario_id)
            tiene_permiso = False
            membresias = (reqSession.get(api_url)).json()
            for membresia in membresias:
                api_url = 'http://localhost:8080/bonita/API/identity/role/'+ membresia['role_id']
                rol = (reqSession.get(api_url)).json()
                if (rol['name'].lower() == permission):
                    tiene_permiso = True
                    break
            return tiene_permiso
    else:
        return False
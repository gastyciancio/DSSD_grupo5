from flask import redirect, render_template, request, url_for, abort, session, flash
from app.db import connection
from app.helpers.auth import authenticated
import requests


def login():
    user = authenticated(session)
    if not user:
        return render_template("auth/login.html")
    else:
        return redirect(url_for("home"))


def authenticate():
    conn = connection()
    params = request.form
    username = params["username"]
    password = params["password"]
    reqSession = requests.Session()

    api_url = 'http://localhost:8080/bonita/loginservice'
    headers =  {'Content-Type':'application/x-www-form-urlencoded'}
    body = {'username': username, 'password': password, 'redirect': False}

    #reqSession queda cargada con las cookies de la respuesta del post
    res = reqSession.post(api_url, data=body, headers=headers)

    if(res.status_code < 200 or res.status_code > 299):
        print("Fallo en el login", flush=True)
        flash("Usuario o contraseña incorrecta")
        return redirect(url_for("auth_login"))
    else:
        print("login exitoso", flush=True)
        session['X-Bonita-API-Token'] = reqSession.cookies.get('X-Bonita-API-Token')
        session['username'] = username
        session['password'] = password
        return redirect(url_for("home"))

def logout():
    user = authenticated(session)
    if not user:
        abort(401)
    del session["username"]
    del session["password"]
    session.clear()
    flash("La sesión se cerró correctamente")

    return redirect(url_for("auth_login"))

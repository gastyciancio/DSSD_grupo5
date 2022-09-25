from flask import redirect, render_template, request, url_for, abort, session, flash
from app.db import connection
from app.models.usuario import Usuario
from app.helpers.auth import authenticated


def login():
    user = authenticated(session)
    if not user:
        return render_template("auth/login.html")
    else:
        return redirect(url_for("home"))


def authenticate():
    conn = connection()
    params = request.form
    email = params["email"]
    password = params["password"]
    user = Usuario.find_user_by_email_first(email)
    if user and user.verify_password(user, password):
        # sesion iniciada correctamente
        session["user"] = user.email
        session["id"] = user.id
        flash("la sesion se inicio correctamente")
        return redirect(url_for("home"))
    else:
        # mail o contraseña invalidos
        flash("usuario o clave incorrecta")
        return redirect(url_for("auth_login"))

def logout():
    user = authenticated(session)
    if not user:
        abort(401)
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("auth_login"))

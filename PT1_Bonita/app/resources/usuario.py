from datetime import datetime
from flask import redirect, render_template, request, url_for, session, abort, flash
from app.db import db
from datetime import datetime
from app.models.roles import Rol
from app.models.usuario import Usuario
from app.models.usuario_tiene_rol import usuario_tiene_rol
from app.helpers.auth import authenticated, check_permission
from app.helpers.paginator import Paginator
from email_validator import validate_email, EmailNotValidError

# Protected resources
def index():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))

def create():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_new"):
        abort(401)


def update(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_update"):
        abort(401)


def delete(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_destroy"):
        abort(401)

def activar(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))


def show(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_show"):
        abort(401)

def verPerfil():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if (not check_permission(session["id"],"usuario_perfil")):
       abort(401)


def updatePassword(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))

def updatePerfil(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
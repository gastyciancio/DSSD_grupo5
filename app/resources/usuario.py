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
    if not check_permission(session["id"], "usuario_index"):
        abort(401)
    conf = Configuracion.get_configs()
    params = request.args
    currentPage = int(params.get("page", 0))

    usuariosTotal = Usuario.dame_todo(
        conf, currentPage, params.get("statusF", None), params.get("nombreF", None)
    )
    roles = Rol.query.all()
    return render_template(
        "usuarios/usuarios.html",
        paginator=Paginator(usuariosTotal, conf.maxElementos, currentPage),
        roles=roles,
    )


def create():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_new"):
        abort(401)
    params = request.form
    roles = request.form.getlist("my_checkbox")
    mensaje = ValidarForm(params)
    if mensaje.validate() == False:
        print("Hay algo mal en el formulario")
    else:
        try:
            valid = validate_email(params["email"])
        except EmailNotValidError as e:
            print(str(e))
            return redirect(url_for("usuarios_index"))
        email = params["email"]
        username = params["username"]
        existeMail = Usuario.find_by_email(email)
        existeUserName = Usuario.find_by_username(username)
        now = datetime.now()
        if existeMail == 0 and existeUserName == 0:
            if not roles:
                mensaje = "debe seleccionar un rol"
            else:
                new_usuario = Usuario(
                    email=params["email"],
                    username=params["username"],
                    password=params["password"],
                    activo=1,
                    updated_at=now,
                    created_at=now,
                    first_name=params["name"],
                    last_name=params["lastname"],
                )
                db.session.add(new_usuario)
                db.session.commit()
                for rol in roles:
                    rol1 = usuario_tiene_rol(usuario_id=new_usuario.id, rol_id=rol)
                    db.session.add(rol1)
                    db.session.commit()
                mensaje = "Se agrego el usuario"
        else:
            if existeMail != 0:
                mensaje = "El mail ya esta en uso, elija otro"
            if existeUserName != 0:
                mensaje = "El nombre de usuario ya esta en uso, elija otro"
        flash(mensaje)
    return redirect(url_for("usuario_index"))


def update(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_update"):
        abort(401)
    lista = []
    listaRoles = request.form.getlist("my_checkbox")
    usuario_to_update = Usuario.find_by_id(id)
    roles_usuario_to_update = usuario_tiene_rol.find_by_id_lista(id)
    roles = Rol.query.all()
    for rol in roles_usuario_to_update:
        lista.append(rol.rol_id)

    if request.method == "POST":
        params = request.form
        existeMail = Usuario.existe_mail(params["email"], id)
        existeUsername = Usuario.existe_username(params["username"], id)
        lista = request.form.getlist("checkbox")

        if existeMail == 0 and existeUsername == 0 and len(listaRoles) != 0:
            usuario_to_update.email = params["email"]
            usuario_to_update.username = params["username"]
            usuario_to_update.updated_at = datetime.now()
            usuario_to_update.first_name = params["name"]
            usuario_to_update.last_name = params["lastname"]
            db.session.commit()
            TodosLosroles = Rol.query.all()
            for rol in TodosLosroles:
                if str(rol.id) in listaRoles:
                    if usuario_tiene_rol.find_by_id(id, rol.id) == 0:  # si no es admin
                        rol1 = usuario_tiene_rol(
                            usuario_id=usuario_to_update.id, rol_id=rol.id
                        )
                        db.session.add(rol1)
                        db.session.commit()
                else:
                    if (
                        usuario_tiene_rol.find_by_id(id, rol.id) != 0
                    ):  # si  es administrador
                        rol_a_borrar = usuario_tiene_rol.esOperador1(id, rol.id)
                        db.session.delete(rol_a_borrar)
                        db.session.commit()
            mensaje = "Se modifico el usuario"
            flash(mensaje)
            return redirect(url_for("usuario_index"))
        else:
            if existeMail != 0:
                mensaje = "El mail ingresado ya existe"
            if existeUsername != 0:
                mensaje = "El nombre de usuario ingresado ya existe"
            if len(listaRoles) == 0:
                mensaje = "No se puede dejar a un usuario sin roles"
            flash(mensaje)
            return render_template(
                "usuarios/update.html",
                usuario=usuario_to_update,
                listaroles=roles,
                roles=lista,
            )
    else:
        return render_template(
            "usuarios/update.html",
            usuario=usuario_to_update,
            listaroles=roles,
            roles=lista,
        )


def delete(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_destroy"):
        abort(401)
    usuario_to_delete = Usuario.find_by_id(id)
    if usuario_to_delete.activo == 0:
        mensaje = "el usuario ya se encuentra borrado"
    else:
        esAdministrador = usuario_tiene_rol.find_by_id(id, 2)
        if esAdministrador != 0:
            mensaje = "No se puede eliminar a un usuario administrador"
        else:
            usuario_to_delete.activo = 0
            db.session.commit()
            mensaje = "El usuario se ha eliminado con exito"
    flash(mensaje)
    return redirect(url_for("usuario_index"))


def activar(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))

    usuario_to_activate = Usuario.find_by_id(id)
    if usuario_to_activate.activo == 1:
        mensaje = "el usuario ya se encuentra borrado"
    else:
        usuario_to_activate.activo = 1
        db.session.commit()
        mensaje = "El usuario se ha activado con exito"
    flash(mensaje)
    return redirect(url_for("usuario_index"))


def show(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if not check_permission(session["id"], "usuario_show"):
        abort(401)
    u = Usuario.query.get_or_404(id)

    return render_template("usuarios/show.html", usuario=u)


def verPerfil():
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    if (not check_permission(session["id"],"usuario_perfil")):
       abort(401)
    email=session["user"]
    u=Usuario.find_user_by_email(email)
    return render_template("usuarios/perfil.html", usuario=u)


def updatePassword(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    usuario_to_update = Usuario.find_by_id(id)

    if request.method == "POST":
        params = request.form
        if usuario_to_update.verify_password(usuario_to_update, params["password"]):
            flash("la nueva contraseña debe ser diferente")
            return render_template("usuarios/perfil.html", usuario=usuario_to_update)
        else:
            usuario_to_update.password = usuario_to_update.create_password(
                params["password"]
            )
            db.session.commit()
            flash("El usuario se ha modificado con exito")
            return redirect(url_for("home"))
    else:
        return render_template("usuarios/perfil.html", usuario=usuario_to_update)


def updatePerfil(id):
    user = authenticated(session)
    if not user:
        return redirect(url_for("auth_login"))
    usuario_to_update = Usuario.find_by_id(id)

    if request.method == "POST":
        params = request.form
        mensaje = ValidarForm(params)
        if mensaje.validate() == False:
            print(
                "Hay algo mal en el formulario"
            )  # En realidad aca se haria un abort ya que algun dato esta mal ingresado
            return render_template("usuarios/perfil.html", usuario=usuario_to_update)
        else:
            existeMail = Usuario.existe_mail(params["email"], id)
            existeUsername = Usuario.existe_username(params["username"], id)
            if existeMail == 0 and existeUsername == 0:
                usuario_to_update.email = params["email"]
                usuario_to_update.username = params["username"]
                # if  usuario_to_update.password != params["password"]:
                #   usuario_to_update.password=usuario_to_update.create_password(params["password"])
                usuario_to_update.updated_at = datetime.now()
                usuario_to_update.first_name = params["name"]
                usuario_to_update.last_name = params["lastname"]
                db.session.commit()
                flash("El usuario se ha modificado con exito")
                return redirect(url_for("home"))
            else:
                if existeMail != 0:
                    mensaje = "El mail ingresado ya existe"
                if existeUsername != 0:
                    mensaje = "El nombre de usuario ingresado ya existe"
                flash(mensaje)
                return render_template(
                    "usuarios/perfil.html", usuario=usuario_to_update
                )
    else:
        return render_template("usuarios/perfil.html", usuario=usuario_to_update)
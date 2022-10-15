from app.db import db
from sqlalchemy import Column, Integer, String, DateTime
from app.models import usuario_tiene_rol
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy.orm import relationship
from app.models.usuario_tiene_rol import usuario_tiene_rol


class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    updated_at = Column(DateTime)
    created_at = Column(DateTime)
    first_name = Column(String(255))
    last_name = Column(String(255))
    roles = relationship(
        "Rol", secondary=usuario_tiene_rol.__tablename__, backref="usuarios"
    )

    @classmethod
    def verify_password(cls, user, password):
        query = check_password_hash(user.password, password)
        return query

    @classmethod
    def create_password(cls, password):
        return generate_password_hash(password)

    @classmethod
    def find_by_email(cls, mail):
        return cls.query.filter_by(email=mail).count()

    @classmethod
    def find_by_username(cls, usern):
        return cls.query.filter_by(username=usern).count()

    @classmethod
    def find_by_id(cls, id1):
        return cls.query.filter_by(id=id1).one()

    @classmethod
    def find_by_id_first(cls, id1):
        return cls.query.filter_by(id=id1).first()

    @classmethod
    def existe_mail(cls, nombree, idPunto=None):
        return cls.query.filter(cls.email == nombree, cls.id != idPunto).count()

    @classmethod
    def existe_username(cls, nombre, idPunto=None):
        return cls.query.filter(cls.username == nombre, cls.id != idPunto).count()

    @classmethod
    def find_user_by_email(cls, e):
        return cls.query.filter_by(email=e).one()

    @classmethod
    def find_user_by_email_first(cls, e):
        return cls.query.filter_by(email=e).first()

    @classmethod
    def dame_todo(csl, conf, page, nombre):
        query = csl.query
        query = query.order_by(csl.username)
        if nombre != None:
            query = query.filter_by(username=nombre)

        return query

    @classmethod
    def find_by_email_and_pass(cls, conn, email, password):
        return cls.query.filter_by(email=email, password=password).first()

    @classmethod
    def has_permission(cls, aUserID, aPermission):
        usuario = Usuario.find_by_id_first(aUserID)
        lista = []
        for rol in usuario.roles:
            for permiso in rol.permisos:
                lista.append(permiso.nombre)
        if aPermission in lista:
            return True
        else:
            return False

    def as_dict(self):
        return {
                "email":        self.email,
                "username":     self.username,
                "firstname":    self.first_name
                }

    def __init__(self,email=None,username=None,password=None,updated_at=None,created_at=None,first_name=None,last_name=None):
        self.email=email
        self.username=username
        if(password!=None):
            self.password=self.create_password(password)
        self.updated_at=updated_at
        self.created_at=created_at
        self.first_name=first_name
        self.last_name=last_name

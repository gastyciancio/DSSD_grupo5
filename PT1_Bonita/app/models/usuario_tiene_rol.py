from sqlalchemy.sql.schema import ForeignKey
from app.db import db
from sqlalchemy import Column


class usuario_tiene_rol(db.Model):
    __tablename__ = "usuario_tiene_rol"
    usuario_id = Column(ForeignKey("Usuario.id"), primary_key=True)
    rol_id = Column(ForeignKey("Rol.id"), primary_key=True)

    @classmethod
    def find_by_id(cls, id1, rol):  # devuelve la cantidad de administradores de un usuario (0 o 1)
        return cls.query.filter_by(usuario_id=id1, rol_id=rol).count()

    @classmethod
    def find_by_id2(cls, id1):  # devuelve la cantidad de operadores de un usuario (0 o 1)
        return cls.query.filter_by(usuario_id=id1, rol_id=1).count()

    @classmethod
    def find_by_id_lista(cls, id1):  # devuelve una lista con todos los roles de un usuario
        query = cls.query.filter_by(usuario_id=id1).all()
        return query

    @classmethod
    def esOperador1(cls, id1, rol):
        return cls.query.filter_by(usuario_id=id1, rol_id=rol).one()


def __init__(self, usuario_id=None, rol_id=None):
    self.usuario_id = usuario_id
    self.rol_id = rol_id

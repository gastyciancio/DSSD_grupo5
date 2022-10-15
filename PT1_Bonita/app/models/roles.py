from flask_sqlalchemy import model
from app.db import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.permiso import Permiso

from app.models.rol_tiene_permiso import rol_tiene_permiso


class Rol(db.Model):
    __tablename__ = "Rol"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255), unique=True)
    permisos = relationship(
        Permiso, secondary=rol_tiene_permiso.__tablename__, backref="roles"
    )


def __init__(self, id=None, nombre=None):
    self.id = id
    self.nombre = nombre
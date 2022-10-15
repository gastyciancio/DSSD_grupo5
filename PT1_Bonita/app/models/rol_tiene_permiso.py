from sqlalchemy.sql.schema import ForeignKey
from app.db import db
from sqlalchemy import Column


class rol_tiene_permiso(db.Model):
    __tablename__ = "rol_tiene_permiso"
    rol_id = Column(ForeignKey("Rol.id"), primary_key=True)
    permiso_id = Column(ForeignKey("Permiso.id"), primary_key=True)


def __init__(self, rol_id=None, permiso_id=None):
    self.rol_id = rol_id
    self.permiso_id = permiso_id
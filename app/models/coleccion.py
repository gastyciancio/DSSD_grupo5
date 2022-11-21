from app.db import db
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from app.models.model import Model #dejarlo


class Coleccion(db.Model):
    __tablename__="coleccion_table"
    id=Column(Integer,primary_key=True)
    tipo=Column(String(255))
    descripcion=Column(String(255))
    nombre=Column(String(255))
    fecha=Column(String(255))
    images = relationship("Image", backref="coleccion")
    models = relationship("Model", backref="coleccion")
    rutas = relationship("Ruta", backref="coleccion")

    def __init__(self,tipo=None,descripcion=None,nombre=None,fecha=None):
        self.tipo=tipo
        self.descripcion=descripcion
        self.nombre=nombre
        self.fecha=fecha

    @classmethod
    def getAll(cls):
        return Coleccion.query.all()

    @classmethod
    def save_collection(cls, params):

        new_collection = Coleccion(
            nombre=params['model_name'],
            descripcion=params['description'],
            fecha=params['fecha'],
            tipo=params['glasses_type']
        )

        db.session.add(new_collection)
        db.session.commit()

        return new_collection
    
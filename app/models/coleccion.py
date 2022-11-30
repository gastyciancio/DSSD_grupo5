from app.db import db
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from app.models.model import Model #dejarlo
from app.models.material import Material


class Coleccion(db.Model):
    __tablename__="coleccion_table"
    id=Column(Integer,primary_key=True)
    nombre=Column(String(255))
    descripcion=Column(String(255))    
    fecha=Column(String(255))
    case_id=Column(String(255))
    images = relationship("Image", backref="coleccion")
    models = relationship("Model", backref="coleccion")
    rutas = relationship("Ruta", backref="coleccion")
    materiales = relationship("Material", backref="coleccion")

    def __init__(self, nombre=None, descripcion=None,fecha=None, case_id=None):
        self.nombre=nombre
        self.descripcion=descripcion        
        self.fecha=fecha
        self.case_id=case_id

    @classmethod
    def getAll(cls):
        return Coleccion.query.all()

    @classmethod
    def findCollectionById(cls, id):
        return Coleccion.query.get(id)
    
    @classmethod
    def findCollectionByCaseId(cls, case_id_collections_active): 
        return Coleccion.query.filter(Coleccion.case_id.in_(case_id_collections_active)).all()

    @classmethod
    def save_collection(cls, params):
        new_collection = Coleccion(
            nombre=params['model_name'],
            descripcion=params['description'],
            fecha=params['fecha'],
            case_id=params['case_id']
        )

        db.session.add(new_collection)
        db.session.commit()

        return new_collection
    
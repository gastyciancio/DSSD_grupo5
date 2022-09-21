from app.db import db
from sqlalchemy import Column,Integer,String


class Coleccion(db.Model):
    __tablename__="coleccion_table"
    id=Column(Integer,primary_key=True)
    tipo=Column(String(255))
    descripcion=Column(String(255))
    nombre=Column(String(255))
    fecha=Column(String(255))
    #archivos=Column(String(255))

    def __init__(self,tipo=None,descripcion=None,nombre=None,fecha=None):
        self.tipo=tipo
        self.descripcion=descripcion
        self.nombre=nombre
        self.fecha=fecha
        #self.archivos=archivos
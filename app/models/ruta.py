from app.db import db
from sqlalchemy import Column,Integer,String,ForeignKey


class Ruta(db.Model):
    __tablename__="ruta"
    id=Column(Integer,primary_key=True)
    ruta=Column(String(255))
    coleccion_id = Column(Integer, ForeignKey("coleccion_table.id"))
    

    def __init__(self,ruta=None):
        self.ruta=ruta

    @classmethod
    def getAll(cls):
        return Ruta.query.all()

    @classmethod
    def save_ruta(cls, ruta,coleccion_id):

        new_ruta = Ruta(
            ruta=ruta,
        )
        new_ruta.coleccion_id = coleccion_id

        db.session.add(new_ruta)
        db.session.commit()

        return new_ruta
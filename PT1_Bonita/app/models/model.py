from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db import db

class Model(db.Model):
    __tablename__="collection_model"
    id = db.Column(db.Integer,primary_key=True)
    name = Column(Text, nullable=False)
    lens_material = Column(Text, nullable=False)
    frame_material = Column(Text, nullable=False)
    coleccion_id = Column(Integer, ForeignKey("coleccion_table.id"))
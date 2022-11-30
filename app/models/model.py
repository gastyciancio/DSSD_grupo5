from sqlalchemy import Column, Integer, Text, ForeignKey, String
from app.db import db

class Model(db.Model):
    __tablename__="collection_model"
    id = db.Column(db.Integer,primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(255))
    coleccion_id = Column(Integer, ForeignKey("coleccion_table.id"))

    def __init__(self, name=None, description=None, type=None, collection_id=None):
        self.name=name 
        self.description=description
        self.type=type
        self.coleccion_id=collection_id

    @classmethod
    def save_model(cls, dict, keys, id_collection):
        new_model = Model(
            name=dict[keys[0]],
            description=dict[keys[1]],
            type=dict[keys[2]],
            collection_id=id_collection
        )
        print(new_model, flush=True)
        db.session.add(new_model)
        db.session.commit()

        return new_model
    
    @classmethod
    def delete_models(cls,id_collection):

        models_of_collections = Model.query.all()

        for model in models_of_collections:
            if model.coleccion_id == id_collection:
                db.session.delete(model)
        db.session.commit()
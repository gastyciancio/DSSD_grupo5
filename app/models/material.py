from sqlalchemy import Column, Integer, Text, ForeignKey
from app.db import db

class Material(db.Model):
    __tablename__="material"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False)
    coleccion_id = Column(Integer, ForeignKey("coleccion_table.id"))

    def __init__(self, name=None, amount=None, collection_id=None):
        self.name = name    
        self.amount = amount
        self.coleccion_id = collection_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
        }
    @classmethod
    def get_material(cls):
        return Material.query.all()

    @classmethod
    def save_material(cls, name_material, amount_material, collection_id_material):
        new_material = Material(
            name=name_material,
            amount=amount_material,
            collection_id=collection_id_material
        )
        print(new_material, flush=True)
        db.session.add(new_material)
        db.session.commit()

        return new_material
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from db import db
from flask import jsonify

class Supplier(db.Model):
    __tablename__="supplier"
    id = Column(Integer,primary_key=True)
    name = Column(Text, nullable=False)
    materials = relationship("SupplierMaterial")


    @classmethod
    def get_suppliers(cls):
        return Supplier.query.all()

    
    def json(self):
        materials = [ material.json() for material in self.materials ]

        return {
            'id': self.id,
            'name': self.name,
            'materials' : materials
        }
from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.models.material import Material
from db import db

class SupplierMaterial(db.Model):
    __tablename__ = "supplier_material"
    supplier_id = Column(ForeignKey("supplier.id"), primary_key=True)
    material_id = Column(ForeignKey("material.id"), primary_key=True)
    price_per_kg = Column(Float, nullable=False)
    #max_deliver_date
    material = relationship("Material")

    def json(self):
        return {
            'id': self.material.id,
            'name': self.material.name,
            'price_per_kg': self.price_per_kg,
            #'material': self.material.json()
        }
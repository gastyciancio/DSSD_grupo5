from sqlalchemy import Column, ForeignKey, Integer, Text, Float, null
from db import db

class Material(db.Model):
    __tablename__="material"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
        }
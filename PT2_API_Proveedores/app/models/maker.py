from sqlalchemy import Column, ForeignKey, Integer, Text
from db import db

class Maker(db.Model):
    __tablename__="maker"
    id = Column(Integer,primary_key=True)
    name = Column(Text, nullable=False)
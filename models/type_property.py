from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base



class TypeProperty(Base):
    __tablename__ = 'type_property'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
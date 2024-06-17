from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer)
    name = Column(String(20))
    built_in = Column(Integer)
    price = Column(Float)
    description = Column(String(100))
    facility = Column(String(50))
    photos = Column(String(200))
    type = Column(Integer)
    current_state = Column(String(10))
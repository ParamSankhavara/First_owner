from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(20))
    built_in = Column(Integer)
    price = Column(Float)
    description = Column(String(100))
    area = Column(String(15))
    bathroom = Column(Integer)
    bedroom = Column(Integer)
    parking = Column(Integer)
    address = Column(String(100))
    facility = Column(String(50))
    photos = Column(String(200))
    type = Column(Integer)
    current_state = Column(String(10))
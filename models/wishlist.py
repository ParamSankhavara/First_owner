from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Wishlist(Base):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer)
    user_id = Column(Integer)
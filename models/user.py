from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True,autoincrement=True)
    role_id = Column(Integer)
    username = Column(String(10))
    mobile_no = Column(Integer, unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))
    updated_on = Column(DateTime)
    created_on = Column(DateTime)
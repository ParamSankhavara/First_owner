from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BuilderInfo(Base):
    __tablename__ = 'builder_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    company_name = Column(String(80), unique=True)
    company_objective = Column(String(50))
    city_of_office = Column(String(10))
    company_achievement = Column(String(200))
    company_since = Column(Integer)
    company_experience = Column(Integer)
    projects_count = Column(Integer)
    running_projects = Column(Integer)
    upcoming_projects = Column(Integer)
    logo = Column(String(100))
    company_pic = Column(String(100))

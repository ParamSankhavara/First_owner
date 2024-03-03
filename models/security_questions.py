from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SecurityQuestion(Base):
    __tablename__ = 'security_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    question_id = Column(Integer)
    answer = Column(String(10))
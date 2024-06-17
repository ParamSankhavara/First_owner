from fastapi import FastAPI,Request
from routes.login import login
from config.con import *
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware
import env
from fastapi_sqlalchemy import DBSessionMiddleware,db
from config.db import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

print(env.DB_ENV)

app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DBSessionMiddleware, db_url=SQLALCHEMY_DATABASE_URI)


engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

for file in os.listdir(PATH): 
    if file.endswith('.py'):
        module_x =file.replace('.py','')
        module = importlib.import_module(f'routes.{module_x}', package=f'{module_x}')
        app.include_router(getattr(module,module_x))
# app.include_router(login)
        

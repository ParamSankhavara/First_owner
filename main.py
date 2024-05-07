from fastapi import FastAPI
from routes.login import login
from dotenv import load_dotenv
from config.con import *
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for file in os.listdir(PATH): 
    if file.endswith('.py'):
        module_x =file.replace('.py','')
        module = importlib.import_module(f'routes.{module_x}', package=f'{module_x}')
        app.include_router(getattr(module,module_x))
# app.include_router(login)
        

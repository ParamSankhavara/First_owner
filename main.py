from fastapi import FastAPI
from routes.login import login
from dotenv import load_dotenv
from config.con import *
import os
import importlib


load_dotenv()


app= FastAPI()


for file in os.listdir(PATH): 
    if file.endswith('.py'):
        module_x =file.replace('.py','')
        module = importlib.import_module(f'routes.{module_x}', package=f'{module_x}')
        app.include_router(getattr(module,module_x))
# app.include_router(login)
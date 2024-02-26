from fastapi import APIRouter,Request
from config.db import db1,engine
from models.user import User
from config.db import db1,engine
from sqlalchemy import text

login = APIRouter()


@login.post('/login')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['username','password']:
        if i not in json_data.keys():
            return {"status":500,"message":f"{i} is missing","data":{}}
        if len(json_data[i]) == 0:
            return {"status":500,"message":f"{i} can not be empty","data":{}}
    data = [row._asdict() for row in db1.execute(text("SELECT * FROM users")).all()]
    print(data,flush=True)
    return {"status":"done"}

@login.post('/logout')
async def login_fuct(request : Request):
    json_data = await request.json()
    print(json_data,flush=True)
    return {"success":"done"}
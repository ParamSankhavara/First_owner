from fastapi import APIRouter,Request
from config.db import db1,engine
from models.user import User
from config.db import db1,engine
from sqlalchemy import text
from uuid import uuid4
from models.session import Session
from utiles.decorater import get_user_data,set_session

login = APIRouter()


@login.post('/login')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['mobile_no','password','role_id']:
        if i not in json_data.keys():
            return {"status":500,"message":f"{i} is missing","data":{}}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":500,"message":f"{i} can not be empty","data":{}}
        else:
            if len(json_data[i]) == 0:
                return {"status":500,"message":f"{i} can not be empty","data":{}}
    user_data = get_user_data(json_data['mobile_no'],json_data['password'],json_data['role_id'])
    if len(user_data) == 0:
        return {"status":200,"message":"Mobile no or password is wrong","data":{}}
    user_data = user_data[0]
    del user_data['_sa_instance_state']
    rand_token = uuid4()
    set_session(user_data['id'],rand_token)
    user_data['token'] = rand_token
    return {"status":200,"message":"Login success","data":user_data}

@login.post('/logout')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['user_id']:
        if i not in json_data.keys():
            return {"status":500,"message":f"{i} is missing","data":{}}
        if len(json_data[i]) == 0:
            return {"status":500,"message":f"{i} can not be empty","data":{}}
    db1.query(Session).filter(Session.user_id == json_data['user_id']).delete()
    db1.commit()
    return {"success":200,"message":"Logout success","data":{}}
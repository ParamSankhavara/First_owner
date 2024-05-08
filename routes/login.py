from fastapi import APIRouter,Request
from config.db import db1,engine
from models.user import User
from config.db import db1,engine
from sqlalchemy import text
from uuid import uuid4
from models.session import Session
from models.security_questions import SecurityQuestion
from utiles.decorater import get_user_data,set_session,validate_request
from sqlalchemy import and_
import datetime
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.questions import Questions

login = APIRouter()


@login.get('/test')
async def test():
    return {"status":200,"message":"Success","data":{}}

@login.post('/login')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['mobile_no','password','role_id']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data[i]) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    user_data = get_user_data(json_data['mobile_no'],json_data['password'],json_data['role_id'])
    if len(user_data) == 0:
        return {"status":0,"message":"Mobile no or password is wrong"}
    user_data = user_data[0]
    rand_token = uuid4()
    set_session(user_data['id'],rand_token)
    user_data['token'] = rand_token
    return JSONResponse(content={"status":1,"message":"Login success","data":user_data})


@login.post('/logout')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['user_id']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if len(json_data[i]) == 0:
            return {"status":0,"message":f"{i} can not be empty"}
    db1.query(Session).filter(Session.user_id == json_data['user_id']).delete()
    db1.commit()
    return JSONResponse(content={"success":1,"message":"Logout success"})


@login.post('/change_password')
@validate_request
async def change_password(request : Request):
    json_data = await request.json()
    for i in ['user_id','old_password','new_password']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data[i]) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    if len([i.__dict__ for i in db1.query(User).filter(and_(User.id == int(json_data['user_id']),User.password == json_data['old_password']))]) != 0:
        db1.query(User).filter(User.id == int(json_data['user_id'])).update({User.password:json_data['new_password']})
        db1.commit()
        return JSONResponse(content={"status":1,"message":"Password changed successfully"})
    else:
        return JSONResponse(content={"status":0,"message":"Old password is wrong"})
 

@login.post('/forgot_password')
@validate_request
async def forgot_password(request : Request):
    json_data = await request.json()
    for i in ['user_id','new_password']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data[i]) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    db1.query(User).filter(User.id == int(json_data['user_id'])).update({User.password:json_data['new_password']})
    db1.commit()
    return JSONResponse(content={"status":1,"message":"Password changed successfully"})


@login.post('/register_user')
async def register_user(request : Request):
    json_data = await request.json()
    for i in ['username','mobile_no','password','role_id','email']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data[i]) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    if len([i.__dict__ for i in db1.query(User).filter(and_(User.mobile_no == json_data['mobile_no'],User.role_id == json_data['role_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this mobile no"}
    if len([i.__dict__ for i in db1.query(User).filter(and_(User.email == json_data['email'],User.role_id == json_data['role_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this email"}
    user_insert = User(mobile_no=json_data['mobile_no'],password=json_data['password'],role_id=json_data['role_id'],email=json_data['email'],username=json_data['username'],updated_on=datetime.datetime.now(),created_on=datetime.datetime.now())
    db1.add(user_insert)
    db1.commit()
    db1.add(SecurityQuestion(user_id=user_insert.id,question_id=int(json_data['question_id']),answer=json_data['question_answer']))
    db1.commit()
    user_data = get_user_data(json_data['mobile_no'],json_data['password'],json_data['role_id'])
    rand_token = uuid4()
    set_session(user_id = user_data['id'],token = rand_token)
    user_data['token'] = rand_token
    return {"status":1,"message":"User registered successfully","data":user_data}


@login.post('/list_questions')
async def register_user(request : Request):
    qus_list = [i.__dict__ for i in db1.query(Questions)]
    return {"status":1,"message":"Success","data":qus_list}


@login.get('/home')
async def home():
    return 'Welcome to First Owner Backend 1.0!!!',200
    # return {"status":200,"message":"Success","data":{}}
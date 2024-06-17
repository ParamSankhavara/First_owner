from fastapi import APIRouter,Request
# from config.db import db1,engine
from fastapi_sqlalchemy import db
from models.user import User
# from config.db import db1,engine
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
import os
from models.bulider_info import BuilderInfo

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
    rand_token = uuid4()
    set_session(user_data['id'],rand_token)
    user_data['token'] = rand_token
    return {"status":1,"message":"Wellcome In First-Owner!","data":user_data}


@login.post('/logout')
async def login_fuct(request : Request):
    json_data = await request.json()
    for i in ['user_id']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if len(json_data[i]) == 0:
            return {"status":0,"message":f"{i} can not be empty"}
    db.session.query(Session).filter(Session.user_id == json_data['user_id']).update({Session.active:0})
    db.session.commit()
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
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.id == int(json_data['user_id']),User.password == json_data['old_password']))]) != 0:
        db.session.query(User).filter(User.id == int(json_data['user_id'])).update({User.password:json_data['new_password']})
        db.session.commit()
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
    db.session.query(User).filter(User.id == int(json_data['user_id'])).update({User.password:json_data['new_password']})
    db.session.commit()
    return JSONResponse(content={"status":1,"message":"Password changed successfully"})


@login.post('/register_user')
async def register_user(request : Request):
    json_data = await request.json()
    for i in ['username','mobile_no','password','email']:
        if i not in json_data.keys():
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data[i]) == int:
            if json_data[i] == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data[i]) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    json_data['role_id'] = 1
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.mobile_no == json_data['mobile_no'],User.role_id == json_data['role_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this mobile no"}
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.email == json_data['email'],User.role_id == json_data['role_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this email"}
    user_insert = User(mobile_no=json_data['mobile_no'],password=json_data['password'],role_id=json_data['role_id'],email=json_data['email'],username=json_data['username'],updated_on=datetime.datetime.now(),created_on=datetime.datetime.now())
    db.session.add(user_insert)
    db.session.commit()
    db.session.add(SecurityQuestion(user_id=user_insert.id,question_id=int(json_data['question_id']),answer=json_data['question_answer']))
    db.session.commit()
    user_data = get_user_data(json_data['mobile_no'],json_data['password'],json_data['role_id'])
    rand_token = uuid4()
    set_session(user_id = user_data['id'],token = rand_token)
    user_data['token'] = rand_token
    return {"status":1,"message":"User registered successfully","data":user_data}


@login.post('/list_questions')
async def register_user(request : Request):
    qus_list = [i.__dict__ for i in db.session.query(Questions)]
    return {"status":1,"message":"Success","data":qus_list}


@login.get('/home')
async def home():
    return 'Welcome to First Owner Backend 1.0!!!',200


@login.post('/register_builder')
async def register_builder(request : Request):
    json_data = await request.form()
    for i in ['username','mobile_no','password','email','company_name','owner_name','company_objective','city','achievement','year_since',"profile_pic","experiance","logo"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if i not in ['profile_pic','logo']:
            if type(json_data.get(i)) == int:
                if json_data.get(i) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
            else:
                if len(json_data.get(i)) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
    role_id = 2
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.mobile_no == json_data.get('mobile_no'),User.role_id == role_id))]) != 0:
        return {"status":0,"message":"User already assiocated with this mobile no"}
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.email == json_data.get('email'),User.role_id == role_id))]) != 0:
        return {"status":0,"message":"User already assiocated with this email"}
    user_insert = User(mobile_no=json_data.get('mobile_no'),password=json_data.get('password'),role_id=role_id,email=json_data.get('email'),username=json_data.get('username'),updated_on=datetime.datetime.now(),created_on=datetime.datetime.now())
    db.session.add(user_insert)
    db.session.commit()
    profile_pic = json_data.get('profile_pic')
    logo = json_data.get('logo')
    os.makedirs(f"static/profile_pic/{user_insert.id}", exist_ok=True)
    os.makedirs(f"static/logo/{user_insert.id}", exist_ok=True)
    with open(f"static/profile_pic/{user_insert.id}/{str(datetime.datetime.now()).translate(str.maketrans('', '', ':- .'))}.{profile_pic.filename.split('.')[-1]}","wb+") as open_file:
        open_file.write(profile_pic.file.read())
        print(open_file.name)
        profile_pic = open_file.name
    with open(f"static/logo/{user_insert.id}/{str(datetime.datetime.now()).translate(str.maketrans('', '', ':- .'))}.{logo.filename.split('.')[-1]}","wb+") as open_logo:
        open_logo.write(logo.file.read())
        logo = open_logo.name
    builder_info = BuilderInfo(user_id = user_insert.id,company_name = json_data.get('company_name'),company_objective = json_data.get('company_objective'),city_of_office = json_data.get('city'),company_achievement = json_data.get('achievement'),company_since = json_data.get('year_since'),company_experience=json_data.get('experiance'),logo = logo,company_pic = profile_pic,owner_name = json_data.get('owner_name'))
    db.session.add(builder_info)
    db.session.commit()
    user_data = get_user_data(json_data['mobile_no'],json_data['password'],role_id)
    rand_token = uuid4()
    set_session(user_id = user_data['id'],token = rand_token)
    user_data['token'] = rand_token
    return {"status":1,"message":"Builder registered successfully","data":user_data}

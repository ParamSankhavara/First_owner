from fastapi import APIRouter,Request
from utiles.decorater import get_user_data,set_session,validate_request,get_builder_data
# from config.db import db1,engine
from fastapi_sqlalchemy import db
from sqlalchemy import text,and_
import os
import datetime
from models.bulider_info import BuilderInfo
from models.user import User

profile = APIRouter()

@profile.post('/builder/get_profile')
@validate_request
async def get_builder_profile(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    if json_data['builder_id'] != "":
        user_data = get_builder_data(user_id=int(json_data['builder_id']))
        user_data['user_id'] = int(json_data['builder_id'])
    if len(user_data) != 0:
        count_data = [i._asdict() for i in db.session.execute(text(f"""SELECT SUM(CASE WHEN current_state = 1 THEN 1 ELSE 0 END) AS completed_projects,SUM(CASE WHEN current_state = 2 THEN 1 ELSE 0 END) AS running_projects,SUM(CASE WHEN current_state = 3 THEN 1 ELSE 0 END) AS upcoming_projects FROM projects WHERE user_id = "{user_data['user_id']}" """))]
        if len(count_data) != 0:
            count_data = [{k: str(v) for k, v in item.items()} for item in count_data][0]
        else:
            count_data = {"completed_projects":"0","running_projects":"0","upcoming_projects":"0"}
        user_data = {**user_data,**count_data}
        user_data['company_pic'] = f"file/download/{user_data['company_pic']}" if user_data['company_pic'] not in ['None',"",None] else "" 
        user_data['logo'] = f"file/download/{user_data['logo']}" if user_data['logo'] not in ['None',"",None] else "" 
        return {"status":1,"message":"Success","data":user_data}
    else:
        return {"status":0,"message":"No Data Found For This User"}

    

@profile.post('/builder/update_profile')
@validate_request
async def update_builder_profile(request : Request):
    json_data = await request.form()
    print(json_data)
    user_data = get_user_data(token=json_data['token'])
    for i in ['username','mobile_no','email','company_name','owner_name','company_objective','city','achievement','year_since',"experiance"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data.get(i)) == int:
            if json_data.get(i) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data.get(i)) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    role_id = 2
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.mobile_no == json_data['mobile_no'],User.role_id == role_id,User.id != user_data['user_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this mobile no"}
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.email == json_data['email'],User.role_id == role_id,User.id != user_data['user_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this email"}
    builder_info_data = {}
    for i in ['company_name','owner_name','company_objective','city','achievement','year_since',"experiance"]:
        builder_info_data[i] = json_data.get(i)
    builder_info_data['city_of_office'] = builder_info_data.pop('city')
    builder_info_data['company_since'] = builder_info_data.pop('year_since')
    builder_info_data['company_experience'] = builder_info_data.pop('experiance')
    builder_info_data['company_achievement'] = builder_info_data.pop('achievement')
    if json_data.get('profile_pic') != None:
        temp1 = json_data.get('profile_pic')
        os.makedirs(f"static/profile_pic/{user_data['user_id']}", exist_ok=True)
        with open(f"static/profile_pic/{user_data['user_id']}/{str(datetime.datetime.now()).translate(str.maketrans('', '', ':- .'))}.{temp1.filename.split('.')[-1]}","wb+") as open_file:
            open_file.write(temp1.file.read())
            builder_info_data['profile_pic'] = open_file.name
    if json_data.get('logo') != None:
        temp2 = json_data.get('logo')
        os.makedirs(f"static/logo/{user_data['user_id']}", exist_ok=True)
        with open(f"static/logo/{user_data['user_id']}/{str(datetime.datetime.now()).translate(str.maketrans('', '', ':- .'))}.{temp2.filename.split('.')[-1]}","wb+") as open_file:
            open_file.write(temp2.file.read())
            builder_info_data['logo'] = open_file.name
    db.session.query(BuilderInfo).filter(BuilderInfo.user_id == user_data['user_id']).update(builder_info_data)
    db.session.commit()
    user_info = {}
    for i in ['username','mobile_no','email']:
        user_info[i] = json_data.get(i)
    db.session.query(User).filter(User.id == user_data['user_id']).update(user_info)
    db.session.commit()
    return {"status":1,"message":"Profile Updated Succesfully"}


@profile.post('/user/update_profile')
@validate_request
async def update_user_profile(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    role_id = 1
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.mobile_no == json_data['mobile_no'],User.role_id == role_id,User.id != user_data['user_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this mobile no"}
    if len([i.__dict__ for i in db.session.query(User).filter(and_(User.email == json_data['email'],User.role_id == role_id,User.id != user_data['user_id']))]) != 0:
        return {"status":0,"message":"User already assiocated with this email"}
    del json_data['token']
    del json_data['user_id']
    db.session.query(User).filter(User.id == user_data['user_id']).update(json_data)
    db.session.commit()
    return {"status":1,"message":"Profile Updated Succesfully"}

@profile.post('/get_builder_list')
@validate_request
async def get_builder_list(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    builder_data = [i._asdict() for i in db.session.execute(text("SELECT company_name,company_pic,user_id FROM first_owner.builder_info as b_info inner join first_owner.users as user_info on user_info.id = b_info.user_id where user_info.role_id = 2"))]
    builder_data = [{k: str(v) for k, v in item.items()} for item in builder_data]
    for i in builder_data:
        i['company_pic'] = f"file/download/{i['company_pic']}" if i['company_pic'] not in ['None',"",None] else ""
    return {"status":1,"message":"Success","data":builder_data}
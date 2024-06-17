from fastapi import APIRouter,Request, File, Form, UploadFile
# from config.db import db,engine
from fastapi_sqlalchemy import db
from models.project import Projects
from utiles.decorater import validate_request,get_user_data,convert_in_str
from models.type_property import TypeProperty
from sqlalchemy import and_,text
from models.wishlist import Wishlist
from typing import List, Optional,Dict
from fastapi.datastructures import FormData
import datetime
import os

project = APIRouter()

@project.post("/get/property")
@validate_request
async def fetch_all_projects(request : Request):
    json_data = await request.json()
    if 'filter' in json_data and json_data['filter'] in ["True",True]:
        user_data = get_user_data(token=json_data['token'])
        if len(json_data['type']) == 0:
            if json_data['user_id'] == 0:
                data = [i.__dict__ for i in db.session.query(Projects).filter(Projects.user_id == user_data['user_id']).all()]
            else:
                data = [i.__dict__ for i in db.session.query(Projects).filter(Projects.user_id.in_([json_data['user_id'],user_data['user_id']])).all()]
        else:
            if json_data['user_id'] == 0:
                data = [i.__dict__ for i in db.session.query(Projects).filter(and_(Projects.user_id == user_data['user_id'],Projects.type.in_(json_data['type']))).all()]
            else:
                data = [i.__dict__ for i in db.session.query(Projects).filter(and_(Projects.user_id.in_([json_data['user_id'],user_data['user_id']]),Projects.type.in_(json_data['type']))).all()]
    else:
        if len(json_data['type']) == 0:
            if json_data['user_id'] == 0:
                data = [i.__dict__ for i in db.session.query(Projects).all()]
            else:
                data = [i.__dict__ for i in db.session.query(Projects).filter(Projects.user_id == json_data['user_id']).all()]
        else:
            if json_data['user_id'] == 0:
                data = [i.__dict__ for i in db.session.query(Projects).filter(Projects.type.in_(json_data['type'])).all()]
            else:
                data = [i.__dict__ for i in db.session.query(Projects).filter(and_(Projects.user_id == json_data['user_id'],Projects.type.in_(json_data['type']))).all()]
    data = convert_in_str(data)
    # data["photos"] = eval(data['photos'])
    file_list = []
    for i in data:
        i["photos"] = eval(i['photos'])
        for p in i['photos']:
            file_list.append(f"file/download/{p}")
        i['photos'] = str(file_list)
        file_list = []
    return {"status":1,"message":"Success","data":data}

@project.post("/add/property")
@validate_request
async def add_project(request:Request,image1: Optional[UploadFile] = File(None),image2: Optional[UploadFile] = File(None),image3: Optional[UploadFile] = File(None),image4: Optional[UploadFile] = File(None),image5: Optional[UploadFile] = File(None)):
    files = [image1, image2, image3, image4, image5]
    files = [file for file in files if file is not None]
    json_data = await request.form()
    json_data = {key: value for key, value in json_data.items() if not key.startswith('image')}
    for i in ["property_name","price","built_in","description","facility","current_state","type"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data.get(i)) == int:
            if json_data.get(i) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data.get(i)) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    for file in files if files else []:
        print(file.filename)
    # return {"status":1,"message":"Project Added Successfully"}
    user_info = get_user_data(token=json_data['token'])
    json_data['name'] = json_data['property_name']
    del json_data['property_name']
    del json_data["token"]
    json_data['user_id'] = user_info['user_id']
    project_data = Projects(**json_data)
    db.session.add(project_data)
    db.session.commit()
    os.makedirs(f"static/photos/{project_data.id}", exist_ok=True)
    file_list = []
    for i in files:
        with open(f"static/photos/{project_data.id}/{str(datetime.datetime.now()).translate(str.maketrans('', '', ':- .'))}.{i.filename.split('.')[-1]}","wb+") as open_file:
            print()
            open_file.write(i.file.read())
            file_list.append(open_file.name)
    db.session.query(Projects).filter(Projects.id == project_data.id).update({"photos":str(file_list)})
    db.session.commit()
    return {"status":1,"message":"Property Added Successfully"}

@project.post("/edit/property")
@validate_request
async def add_project(request : Request):
    json_data = await request.json()
    for i in ["property_name","price","built_in","description","facility","current_state","type","project_id"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if i not in ["photos"]:
            if type(json_data.get(i)) == int:
                if json_data.get(i) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
            else:
                if len(json_data.get(i)) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
    json_data['name'] = json_data['property_name']
    del json_data['property_name']
    p_id = json_data['project_id']
    del json_data['project_id']
    del json_data["token"]
    db.session.query(Projects).filter(Projects.id == p_id).update(json_data)
    db.session.commit()
    return {"status":1,"message":"Property Updated Successfully"}

@project.post("/get/property_type")
@validate_request
async def get_property_type(request : Request):
    data = [i.__dict__ for i in db.session.query(TypeProperty).all()]
    data = convert_in_str(data)
    return {"status":1,"message":"Success","data":data}


@project.post("/add/wishlist")
@validate_request
async def add_wishlist(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    for i in ["property_id"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if type(json_data.get(i)) == int:
            if json_data.get(i) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
        else:
            if len(json_data.get(i)) == 0:
                return {"status":0,"message":f"{i} can not be empty"}
    wishlist_data = Wishlist(user_id = user_data['user_id'],property_id = json_data['property_id'])
    db.session.add(wishlist_data)
    db.session.commit()
    return {"status":1,"message":"Added To Wishlist"}


@project.post("/get/wishlist")
@validate_request
async def get_wishlist(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    data = [i._asdict() for i in db.session.execute(text(f"""SELECT p.* from first_owner.projects as p inner join first_owner.wishlist as w ON w.property_id = p.id where w.user_id = {user_data['user_id']}"""))]
    data = convert_in_str(data)
    return {"status":1,"message":"Success","data":data}



@project.post("/remove/wishlist")
@validate_request
async def remove_wishlist(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
    db.session.query(Wishlist).filter(Wishlist.user_id == user_data['user_id'],Wishlist.property_id == json_data['property_id']).delete()
    db.session.commit()
    return {"status":1,"message":"Removed Successfully"}
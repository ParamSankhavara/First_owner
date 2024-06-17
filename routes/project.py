from fastapi import APIRouter,Request
# from config.db import db,engine
from fastapi_sqlalchemy import db
from models.project import Projects
from utiles.decorater import validate_request,get_user_data
from models.type_property import TypeProperty

project = APIRouter()

@project.post("/all/projects")
@validate_request
def fetch_all_projects(request : Request):
    data = [i.__dict__ for i in db.session.query(Projects).all()]
    return {"status":200,"message":"Success","data":data}

@project.post("/add/property")
@validate_request
async def add_project(request : Request):
    json_data = await request.json()
    for i in ["property_name","price","built_in","description","area","bathroom","bedroom","parking","address","facility","current_state","photos"]:
        if json_data.get(i) == None:
            return {"status":0,"message":f"{i} is missing"}
        if i not in ["photos"]:
            if type(json_data.get(i)) == int:
                if json_data.get(i) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
            else:
                if len(json_data.get(i)) == 0:
                    return {"status":0,"message":f"{i} can not be empty"}
    user_info = get_user_data(token=json_data['token'])
    json_data['name'] = json_data['property_name']
    del json_data['property_name']
    json_data['user_id'] = user_info['user_id']
    db.add(json_data)
    db.session.commit()
    return {"status":200,"message":"Project Added Successfully"}

@project.post("/edit/property_type")
@validate_request
async def add_project(request : Request):
    json_data = await request.json()
    for i in ["property_name","price","built_in","description","area","bathroom","bedroom","parking","address","facility","current_state","photos"]:
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
    db.session.query(TypeProperty).filter(TypeProperty.id == json_data['id']).update(json_data)
    db.session.commit()
    return {"status":200,"message":"Project Added Successfully"}

@project.post("/get/property_type")
@validate_request
async def get_property_type(request : Request):
    json_data = await request.json()
    data = [i.__dict__ for i in db.session.query(TypeProperty)]
    return {"status":200,"message":"Success","data":data}
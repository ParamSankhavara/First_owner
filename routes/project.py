from fastapi import APIRouter,Request
from config.db import db1,engine
from models.project import Projects
from utiles.decorater import validate_request

project = APIRouter()

@project.post("/all/projects")
@validate_request
def fetch_all_projects(request : Request):
    data = [i.__dict__ for i in db1.query(Projects).all()]
    return {"status":200,"message":"Success","data":data}
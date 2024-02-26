from fastapi import APIRouter,Request
from config.db import db1,engine
from models.project import Projects

project = APIRouter()

@project.post("/all/projects")
def fetch_all_projects(request : Request):
    pass
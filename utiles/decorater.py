# from config.db import db1,engine
from fastapi_sqlalchemy import db
from models.user import User
from models.session import Session
from fastapi_sqlalchemy import db
from sqlalchemy import text,and_
from fastapi import Request
from functools import wraps
import functools


def get_user_data(mobile_no = 0,password = "",role_id = 0,token=""):
    if len(token) == 0:
        data = [i._asdict() for i in db.session.execute(text(f"""
        SELECT 
            u.*,sq.question_id,q.question,sq.answer
        FROM
            users AS u
                LEFT JOIN
            security_question AS sq ON u.id = sq.user_id
                LEFT JOIN
            questions AS q ON q.id = sq.question_id
        WHERE
            mobile_no = '{mobile_no}' AND password = '{password}' AND role_id = {int(role_id)}"""))]
        if len(data) != 0:
            data = {key: str(value) for key, value in data[0].items()}
            return data
        else:
            return {}
    else:
        data = [i._asdict() for i in db.session.execute(text(f"""
        SELECT user_info.*,company_name,company_objective,company_achievement,company_experience,company_pic,company_since,city_of_office,logo,owner_name FROM first_owner.users as user_info inner join first_owner.session as session ON session.user_id = user_info.id left join first_owner.builder_info as b_info on b_info.user_id = session.user_id where token = "{token}" """))]
        print(data)
        if len(data) != 0:
            data = {key:str(value) for key,value in data[0].items()}
            data['user_id'] = data.pop('id')
            return data
        else:
            return {}

def get_builder_data(user_id):
    data = [i._asdict() for i in db.session.execute(text(f"""SELECT user_info.*,company_name,company_objective,company_achievement,company_experience,company_pic,company_since,city_of_office,logo,owner_name FROM first_owner.users AS user_info INNER JOIN first_owner.builder_info AS b_info ON b_info.user_id = user_info.id WHERE
    user_info.id = {user_id}"""))]
    print(data)
    if len(data) != 0:
        data = {key:str(value) for key,value in data[0].items()}
        data['user_id'] = data.pop('id')
        return data
    else:
        return {}


def set_session(user_id,token):
    data = [i.__dict__ for i in db.session.query(Session).filter(Session.user_id == user_id)]
    if len(data) == 0:
        db.session.add(Session(user_id=user_id,token=token,active = 1))
        db.session.commit()
    else:
        db.session.query(Session).filter(Session.user_id == user_id).update({Session.active:0})
        db.session.commit()
        db.session.add(Session(user_id=user_id,token=token,active = 1))
        db.session.commit()
    return None

# Custom decorator to validate the token
def validate_request(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            json_data = await request.json()
            if 'token' not in json_data.keys():
                return {"status":500,"message":"Token Is Missing","data":{}}
            if len([i.__dict__ for i in db.session.query(Session).filter(and_(Session.token == json_data['token'],Session.active == 1))]) == 0:
                return {"status":500,"message":"Invalid token","data":{}}
            return await func(request, *args, **kwargs)
        except RuntimeError:
            json_data = await request.form()
            if json_data.get('token') == None:
                return {"status":500,"message":"Token Is Missing","data":{}}
            if len([i.__dict__ for i in db.session.query(Session).filter(and_(Session.token== json_data.get('token'),Session.active == 1))]) == 0:
                return {"status":500,"message":"Invalid token","data":{}}
            return await func(request, *args, **kwargs)
    return wrapper


def convert_in_str(data):
    return [{key: str(value) for key, value in item.items()} for item in data]
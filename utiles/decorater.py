from config.db import db1,engine
from models.user import User
from models.session import Session
from config.db import db1,engine
from sqlalchemy import text,and_
from fastapi import Request
from functools import wraps
import functools


def get_user_data(mobile_no = 0,password = "",role_id = 0,token=""):
    if len(token) == 0:
        data = [i._asdict() for i in db1.execute(text(f"""
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
            print(data)
            return data
        else:
            return {}
    else:
        data = [i._asdict() for i in db1.execute(text(f"""
        SELECT user.* FROM first_owner.builder_info as user inner join first_owner.session as session ON session.user_id = user.user_id where token = "{token}" """))]
        if len(data) != 0:
            data = {key:str(value) for key,value in data[0].items()}
            return data
        else:
            return {}
    # data = [i.__dict__ for i in db1.query(User).filter(and_(User.mobile_no == mobile_no,User.password == password,User.role_id == role_id))]




def set_session(user_id,token):
    data = [i.__dict__ for i in db1.query(Session).filter(Session.user_id == user_id)]
    if len(data) == 0:
        db1.add(Session(user_id=user_id,token=token,active = 1))
        db1.commit()
    else:
        db1.query(Session).filter(Session.user_id == user_id).update({Session.active:0})
        db1.commit()
    return None

# Custom decorator to validate the token
def validate_request(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        json_data = await request.json()
        if 'token' not in json_data.keys():
            return {"status":500,"message":"Token Is Missing","data":{}}
        if len([i.__dict__ for i in db1.query(Session).filter(and_(Session.token == json_data['token'],Session.active == 1))]) == 0:
            return {"status":500,"message":"Invalid token","data":{}}
        return await func(request, *args, **kwargs)
    return wrapper
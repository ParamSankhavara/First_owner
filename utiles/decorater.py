from config.db import db1,engine
from models.user import User
from models.session import Session
from config.db import db1,engine
from sqlalchemy import text,and_
from fastapi import Request
from functools import wraps
import functools


def get_user_data(mobile_no,password,role_id):
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
    # data = [i.__dict__ for i in db1.query(User).filter(and_(User.mobile_no == mobile_no,User.password == password,User.role_id == role_id))]
    return data


def set_session(user_id,token):
    data = [i.__dict__ for i in db1.query(Session).filter(Session.user_id == user_id)]
    if len(data) == 0:
        db1.add(Session(user_id=user_id,token=token))
        db1.commit()
    else:
        db1.query(Session).filter(Session.user_id == user_id).update({Session.token:token})
        db1.commit()
    return None

# Custom decorator to validate the token
def validate_request(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        json_data = await request.json()
        if len([i.__dict__ for i in db1.query(Session).filter(and_(Session.token == json_data['token'],Session.user_id == json_data['user_id']))]) == 0:
            return {"status":500,"message":"Invalid token","data":{}}
        return await func(request, *args, **kwargs)
    return wrapper
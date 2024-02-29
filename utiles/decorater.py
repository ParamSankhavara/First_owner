from config.db import db1,engine
from models.user import User
from models.session import Session
from config.db import db1,engine
from sqlalchemy import text,and_

def get_user_data(mobile_no,password,role_id):
    data = [i.__dict__ for i in db1.query(User).filter(and_(User.mobile_no == mobile_no,User.password == password,User.role_id == role_id))]
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
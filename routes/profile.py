from fastapi import APIRouter,Request
from utiles.decorater import get_user_data,set_session,validate_request
# from config.db import db1,engine
from fastapi_sqlalchemy import db
from sqlalchemy import text,and_

profile = APIRouter()



# 1 = completed
# 2 = Running
# 3 = upcoming


@profile.post('/builder/get_profile')
@validate_request
async def get_builder_profile(request : Request):
    json_data = await request.json()
    user_data = get_user_data(token=json_data['token'])
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
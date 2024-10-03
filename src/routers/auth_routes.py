from fastapi import APIRouter
from pydantic import BaseModel
from ..auth import Auth

class login_body(BaseModel):
    password:str

auth_router = APIRouter()

@auth_router.post("/employee/{emp_id}")
def login(emp_id:int,body_data:login_body):
    auth_obj = Auth(emp_id,body_data.password)
    
def update_password(employee,new_pass):
    pass

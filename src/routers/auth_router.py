from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated
from fastapi import HTTPException,Depends
from ..auth import Auth
# from passlib.context import CryptContext, CryptPolicy
from jose import JWTError, jwt
from ..types.general_types import Token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

SECRET_KEY = "xH1fIgsTLC8PCN3BQwgFJXvSxx753idA"
ALGORITHM = "HS256"

class login_body(BaseModel):
    password:str

auth_router = APIRouter()


@auth_router.post("/login")
def login(login_form:Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_obj = Auth()
    try:
        auth_token = auth_obj.login(login_form.username,login_form.password) 
        if auth_token :
            return auth_token
        else :
            raise HTTPException(status_code = 401, detail = "Invalid userid or password")
    except Exception as err:
        return err

    finally:
        del auth_obj


token_from_auth_header = OAuth2PasswordBearer(tokenUrl="/login")
 
def validate_token(token:Annotated[str,Depends(token_from_auth_header)]):
    try:
        user = Auth.validate_token(token=token)
        return user

    except JWTError as err:
        raise HTTPException(status_code=400,detail = str(err))

@auth_router.post("/employee/{emp_id}/password")
def update_password(emp_id:int,employee:Annotated[dict,Depends(validate_token)]):
    employee.update_password()

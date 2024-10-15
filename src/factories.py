from fastapi import Depends, HTTPException
from typing import Annotated

from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
from .entities.employee.employee import Employee
from .auth import Auth

from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

token_from_auth_header = OAuth2PasswordBearer(tokenUrl="/login")



def admin_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        return Auth.validate_token_gen_obj({"token": token, "user_type": "admin"})
    except JWTError as err:
        raise HTTPException(status_code=401, detail=str(err))


def hr_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        return Auth.validate_token_gen_obj({"token": token, "user_type": "hr"})
    except JWTError as err:
        raise HTTPException(status_code=401, detail=str(err))


def worker_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        return Auth.validate_token_gen_obj({"token": token, "user_type": "worker"})
    except JWTError as err:
        raise HTTPException(status_code=401, detail=str(err))

def employee_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        return Auth.validate_token_gen_obj({"token":token,"user_type":"basic"})
    except JWTError as err:
        raise HTTPException(status_code=401,detail=str(err))


def user_factory(token:str,allowed_users:list):
    try:
        return Auth.validate_token_gen_obj(token,allowed_users)
    except JWTError as err:
        raise HTTPException(status_code=401,detail=str(err))

# token: Annotated[str, Depends(token_from_auth_header)],user_type:str


# def admin_handler(token: Annotated[str, Depends(token_from_auth_header)]):
#     user_type = "admin"
#     global token_from_auth_header
#     return dict({"token": token, "user_type": user_type})
#
#
# def user_factory(token_obj: Annotated[dict, Depends(admin_handler)]):
#     try:
#         print(token_obj["token"], token_obj["user_type"])
#         # print(token_obj["token"])
#         user = Auth.validate_token_gen_obj()
#         # if isinstance(user, Admin):
#         print(user)
#         # else:
#         #     raise HTTPException(status_code=403)
#     # # return user
#     except JWTError as err:
#         raise HTTPException(status_code=401, detail=str(err))

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
        user = Auth.validate_token_gen_obj(token)
        if isinstance(user, Admin):
            return user
        else:
            raise HTTPException(status_code=403)
    except JWTError as err:
        raise HTTPException(status_code=400, detail=str(err))


def hr_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        user = Auth.validate_token_gen_obj(token)
        if isinstance(user, Hr_employee):
            return user
        else:
            raise HTTPException(status_code=403)
    except JWTError as err:
        raise HTTPException(status_code=400, detail=str(err))


def worker_factory(token: Annotated[str, Depends(token_from_auth_header)]):
    try:
        user = Auth.validate_token_gen_obj(token)
        if isinstance(user, Worker):
            return user
        else:
            raise HTTPException(status_code=403)
    except JWTError as err:
        raise HTTPException(status_code=400, detail=str(err))

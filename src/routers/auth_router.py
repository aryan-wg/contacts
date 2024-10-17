from ..entities.employee.employee import Employee
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated
from fastapi import HTTPException, Depends, Request
from ..auth import Auth
from ..execptions.HttpExceptions import (
    InvalidValueErr,
    InternalServerErr,
    UnauthorizedErr,
)
from ..Logger.Logger import Logger
# from jose import JWTError, jwt
# from ..types.general_types import Token
from ..types.general_types import ChangePassBody

# from ..factories import worker_factory
from fastapi.security import OAuth2PasswordRequestForm
# from ..entities.worker.worker import Worker

################################################################
from ..Test import Test
################################################################

SECRET_KEY = "xH1fIgsTLC8PCN3BQwgFJXvSxx753idA"
ALGORITHM = "HS256"


class login_body(BaseModel):
    password: str


auth_router = APIRouter()


@auth_router.get("/test")
async def test_sqlite():
    # pass
    test = Test()
    return await test.sqlite_multiple_read_write_calls()


@auth_router.post("/login", status_code=200)
async def login(login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_obj = Auth()
    try:
        auth_token = await auth_obj.login(int(login_form.username), login_form.password)
        if auth_token:
            logger = Logger(log_file="logs.log", log_name=f"{login_form.username}")
            logger.log("user logged in")
            return auth_token
        else:
            logger = Logger(log_file="logs.log", log_name=f"{login_form.username}")
            logger.log("login failed")
            raise HTTPException(status_code=401, detail="Invalid userid or password")
    except HTTPException as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        logger = Logger(log_file="logs.log", log_name=f"{login_form.username}")
        logger.log(f"login failed {str(err)}","error")
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        del auth_obj


@auth_router.post("/employee/{emp_id}/password", status_code=204)
async def update_password(emp_id: int, body_data: ChangePassBody, request: Request):
    logger = Logger(log_file="logs.log", log_name=f"{emp_id}")
    employee = Employee(emp_id,logger)
    try:
        await employee.update_password(emp_id,body_data.old_pass, body_data.new_pass)
    except ValueError as err:
        raise UnauthorizedErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del employee

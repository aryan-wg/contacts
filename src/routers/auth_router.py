from ..entities.worker.worker import Worker
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Annotated
from fastapi import HTTPException, Depends
from ..auth import Auth
from jose import JWTError, jwt
from ..types.general_types import Token
from ..types.general_types import ChangePassBody
from ..factories import worker_factory
from fastapi.security import OAuth2PasswordRequestForm

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


@auth_router.post("/login", status_code = 200)
def login(login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_obj = Auth()
    try:
        auth_token = auth_obj.login(login_form.username, login_form.password)
        if auth_token:
            return auth_token
        else:
            print(login_form.username, login_form.password)
            raise HTTPException(status_code = 400, detail="Invalid userid or password")
    except HTTPException as err:
        raise HTTPException(status_code = err.status_code,detail = err.detail)
    # except Exception as err:
    #     raise HTTPException(status_code=500, detial=str(err))
    finally:
        del auth_obj


@auth_router.post("/employee/{emp_id}/password")
def update_password(
    emp_id: int,
    body_data: ChangePassBody,
    employee: Annotated[Worker, Depends(worker_factory)],
):
    employee.update_password(body_data.old_pass, body_data.new_pass, emp_id)
    del employee

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
from ..entities.worker.worker import Worker
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
    print("hello")
    test = Test()
    return await test.sqlite_multiple_read_write_calls()


@auth_router.post("/login", status_code = 200)
async def login(login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print("hello")
    auth_obj = Auth()
    try:
        print("hellooooo")
        auth_token = await auth_obj.login(int(login_form.username), login_form.password)
        if auth_token:
            return auth_token
        else:
            raise HTTPException(status_code = 401, detail="Invalid userid or password")
    except HTTPException as err:
        raise HTTPException(status_code = err.status_code,detail = err.detail)
    except Exception as err:
        raise HTTPException(status_code = 500, detail=str(err))
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

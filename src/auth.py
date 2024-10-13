from abc import abstractmethod

from datetime import datetime, timedelta, timezone
from typing import Annotated
from .types.argument_types import TokenObj
from fastapi import Depends, HTTPException
from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
from .utils.async_pg_db_utils import read_fields_from_record
from .utils.general_utils import check_pass
from datetime import datetime, timezone, timedelta
from .types.general_types import Token
from jose import jwt, JWTError

SECRET_KEY = "xH1fIgsTLC8PCN3BQwgFJXvSxx753idA"
ALGORITHM = "HS256"


class Auth:
    async def login(self, empId, password):
        try:
            print("login ke andar")
            user = await read_fields_from_record("employees", "*", "empid", [empId])
            # user = await read_fields_from_record("employees", "*", "phone", [9999999999])
            print("login ke user lane ke bad",user)
            if user:
                _, name, phone, email, address, hashed_db, user_type = user[0]
                employee_info = (empId, name, phone, email, address)
                check = check_pass(password, hashed_db)
                if check:
                    return self.create_access_token(
                        empId, user_type, timedelta(seconds=100000)
                    )
                else:
                    return None
        except NameError as err:
            raise err
        except Exception as err:
            raise err

    def create_access_token(self, empId: int, user_type: str, expires_delta: timedelta):
        encode = {"empId": empId, "user_type": user_type}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({"exp": expires})
        return Token(
            access_token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM),
            token_type="Bearer",
        )

    @abstractmethod
    def validate_token_gen_obj(token_obj: TokenObj):
        if not token_obj:
            raise HTTPException(status_code=401, detail="Not authenticated")
        else:
            try:
                decoded_token = jwt.decode(
                    token_obj["token"], SECRET_KEY, algorithms=[ALGORITHM]
                )
                if token_obj["user_type"] == decoded_token["user_type"]:
                    match decoded_token["user_type"]:
                        case "admin":
                            return Admin()
                        case "worker":
                            return Worker()
                        case "hr":
                            return Hr_employee()
                else:
                    raise HTTPException(status_code=403, detail="Forbidden")
            except JWTError as err:
                raise HTTPException(status_code=403, detail=str(err))

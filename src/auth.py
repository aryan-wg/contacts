from abc import abstractmethod

from datetime import datetime, timedelta, timezone
from typing import Annotated
from .types.argument_types import TokenObj
from .Logger.Logger import Logger
from fastapi import Depends, HTTPException
from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
from .entities.employee.employee import Employee
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
            user = await read_fields_from_record("employees", "*", "empid", [empId])
            if user:
                _, name, phone, email, address, hashed_db, user_type = user[0]
                # employee_info = (empId, name, phone, email, address)
                check = check_pass(password, hashed_db)
                if check:
                    return self.create_access_token(
                        empId, user_type, timedelta(seconds=100000)
                    )
                else:
                    return None
        except Exception as err:
            raise err

    def create_access_token(self, empId: int, user_type: str, expires_delta: timedelta):
        encode = {"emp_id": empId, "user_type": user_type}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({"exp": expires})
        return Token(
            access_token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM),
            token_type="Bearer",
        )

    @abstractmethod
    def validate_token_gen_obj(token, allowed_user_types,route):
        if not token:
            logger = Logger(log_file="logs.log", log_name=f"UNAUTHENTICATED {route}")
            logger.log(f"validate_token_gen_obj token not found")
            raise HTTPException(status_code=401, detail="Not authenticated")
        else:
            try:
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                logger = Logger(log_file="logs.log",log_name=f"{decoded_token['emp_id']} {route}")
                if decoded_token["user_type"] in allowed_user_types:
                    match decoded_token["user_type"]:
                        case "admin":
                            return Admin(decoded_token["emp_id"],logger)
                        case "worker":
                            return Worker(decoded_token["emp_id"],logger)
                        case "hr":
                            return Hr_employee(decoded_token["emp_id"],logger)
                elif "employee" in allowed_user_types :
                    return Employee(decoded_token["emp_id"],logger)
                else:
                    raise HTTPException(status_code=403, detail=f"Forbidden employee id: {decoded_token['emp_id']}")
            except JWTError as err:
                logger = Logger(log_file="logs.log",log_name=f"UNAUTHENTICATED {route}")
                logger.log(f"validate_token_gen_obj {str(err)}")
                raise HTTPException(status_code=401, detail=str(err))

from abc import abstractmethod

from datetime import datetime,timedelta,timezone
from typing import Annotated
from fastapi import Depends,HTTPException
from .entities.admin.admin import Admin
from .entities.hr.hr_employee import Hr_employee
from .entities.worker.worker import Worker
from .utils.db_utils import read_fields_from_record
from .utils.general_utils import check_pass
from datetime import datetime,timezone,timedelta
from .types.general_types import Token
from jose import jwt,JWTError

SECRET_KEY = "xH1fIgsTLC8PCN3BQwgFJXvSxx753idA"
ALGORITHM = "HS256"



class Auth:

    def login(self,empId,password):
        try:
            user = read_fields_from_record("employees", "*", "empId", [empId])
            if user :
                _,name,phone,email,address,hashed_db,user_type = user[0]
                employee_info = (empId,name,phone,email,address)
                check = check_pass(password,hashed_db)
                if check:
                    return self.create_access_token(empId,user_type,timedelta(seconds=100000))
                else:
                    return None
        except NameError as err:
            return err 

    def create_access_token(self,empId:int,user_type: str, expires_delta: timedelta):
        encode = {"sub": empId,"user_type":user_type}
        expires = datetime.now(timezone.utc) + expires_delta
        encode.update({"exp": expires})
        return Token(access_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM),token_type="Bearer")
    
    @abstractmethod
    def validate_token_gen_obj(token:str,):
        if not token:
            raise HTTPException(status = 401 ,detail = "Not authenticated")
        else:
            try:
                user = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
                match user["user_type"]:
                    case "admin":
                        return Admin()
                    case "worker":
                         return Worker()
                    case "hr":
                         return  Hr_employee()

            except JWTError as err:
                raise HTTPException(status = 403,detail=str(err))


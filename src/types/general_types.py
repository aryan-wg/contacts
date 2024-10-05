from pydantic import BaseModel
from enum import Enum

class UserTypeEnum(str,Enum):
    admin = "admin"
    hr = "hr"
    worker = "worker"

class Token(BaseModel):
    access_token:str
    token_type:str

class Address(BaseModel):
    street: str
    postal_code: int
    city: str
    state: str
    country: str

class EmployeeInfo(BaseModel):
  password: str
  user_type: UserTypeEnum
  name: str
  phone: int
  email: str
  address: Address
  reports_to: int


from pydantic import BaseModel
from .general_types import UserTypeEnum

class TokenObj(BaseModel):
    token:str
    user_type:UserTypeEnum
    
    
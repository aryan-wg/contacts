from fastapi import APIRouter
from pydantic import BaseModel
from ..entities.admin.admin import Admin
import json
from ..types.general_types import EmployeeInfo

employee_router = APIRouter()

@employee_router.post("/",)
def create_employee(new_employee:EmployeeInfo):
    employee_info_dict = new_employee.dict()
    employee_info_dict["address"] = json.dumps(employee_info_dict["address"])
    returned_val = Admin.create_new_employee(employee_info_dict)
    print(returned_val)
    return returned_val

def search_employee_controler(employee,search_str):
    pass

def see_my_profile(employee):
    pass

def request_update_controler(employee,update_info):
    pass



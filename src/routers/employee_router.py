from typing import Annotated

from ..factories import admin_factory
from ..entities.employee.employee import Employee
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..entities.admin.admin import Admin
import json
from ..types.general_types import EmployeeInfo

employee_router = APIRouter()


@employee_router.post("/",status_code = 201)
def create_employee(
    new_employee: EmployeeInfo, admin_obj: Annotated[Admin, Depends(admin_factory)]
):
    employee_info_dict = new_employee.dict()
    employee_info_dict["address"] = json.dumps(employee_info_dict["address"])
    print(employee_info_dict)
    created_emp = admin_obj.create_new_employee(employee_info_dict)
    created_relation = admin_obj.create_new_relation(
        emp_id=created_emp[0], reports_to_emp_id=employee_info_dict["reports_to"]
    )
    if not created_relation:
        admin_obj.delete_employee(created_emp[0])
        raise HTTPException(
            status_code=400, detail="Reporting to employee does not exist"
        )
    else:
        return {
            "success": True,
            "message": "Employee created successfuly",
            "emp_id": created_emp[0],
        }

@employee_router.delete("/{emp_id}")
def remove_employee(emp_id:int,admin_obj: Annotated[Admin,Depends(admin_factory)]):
    admin_obj.remove_employee(emp_id)

# @employee_router.get("/")
# def test(data:EmployeeInfo,admin_obj:Annotated[Admin,Depends(admin_factory)]):
#     print(data)
#     print(admin_obj)


def search_employee_controler(employee, search_str):
    pass


def see_my_profile(employee):
    pass


def request_update_controler(employee, update_info):
    pass

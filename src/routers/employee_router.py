import json

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from ..execptions.CustomExceptions import (
    InvalidValueErr,
    InternalServerErr,
    NotFoundErr,
    NotAllowedError,
)
from ..factories import admin_factory
from ..entities.employee.employee import Employee
from ..entities.admin.admin import Admin
from ..types.general_types import EmployeeInfo

employee_router = APIRouter()


@employee_router.post("/", status_code=201)
async def create_employee(
    new_employee: EmployeeInfo, admin_obj: Annotated[Admin, Depends(admin_factory)]
):
    try:
        employee_info_dict = new_employee.dict()
        employee_info_dict["address"] = json.dumps(employee_info_dict["address"])
        created_emp = await admin_obj.create_new_employee(employee_info_dict)
        created_relation = await admin_obj.create_new_relation(
            emp_id=created_emp[0], reports_to_emp_id=employee_info_dict["reports_to"]
        )
        if not created_relation:
            await admin_obj.delete_employee(created_emp[0])
            raise ValueError("Reporting to employee does not exist")
        else:
            return {
                "success": True,
                "message": "Employee created successfuly",
                "emp_id": created_emp[0],
            }
    except ValueError as err:
        raise InvalidValueErr(err)
    except Exception as err:
        raise InternalServerErr(err)


@employee_router.delete("/{emp_id}", status_code=204)
async def remove_employee(
    emp_id: int, admin_obj: Annotated[Admin, Depends(admin_factory)]
):
    try:
        if await admin_obj.remove_employee(emp_id):
            return True
        else:
            raise ValueError("Employee not found in database")

    except ValueError as err:
        if "not found" in str(err):
            raise NotFoundErr(err)
        else:
            raise NotAllowedError(err)
    except Exception as err:
        raise InternalServerErr(err)


@employee_router.get("/{emp_id}/requests", status_code=200)
async def get_requests(
    emp_id: int, status: str, admin_obj: Annotated[Admin, Depends(admin_factory)]
):
    try:
        status_list = [item.replace(" ","") for item in status.split(",")]
        print(status_list)
        data = await admin_obj.get_req(status_list)
        print(data)
    except ValueError as err:
        raise NotFoundErr(err)
    except Exception as err:
        raise InternalServerErr(err)

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

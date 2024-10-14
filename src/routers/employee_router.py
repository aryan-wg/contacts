import json

from typing import Annotated, final
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from ..utils.general_utils import csv_to_list_of_alpha_num_str

from ..execptions.HttpExceptions import (
    InvalidValueErr,
    InternalServerErr,
    NotFoundErr,
    NotAllowedErr,
    ForbiddenErr,
)
from ..factories import admin_factory, worker_factory, employee_factory
from ..entities.worker.worker import Worker
from ..entities.employee.employee import Employee
from ..entities.admin.admin import Admin
from ..types.general_types import EmployeeInfo, ChangeInfoRequestBody

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
    finally:
        del admin_obj


@employee_router.get("/", status_code=200)
async def search_employee(
    query_username: str,
    baisc_employee_obj: Annotated[Worker, Depends(employee_factory)],
):
    try:
        pass
        data = await baisc_employee_obj.search_other_employee(query_username)
        return data
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del baisc_employee_obj


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
            raise NotAllowedErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del admin_obj


@employee_router.post("/{emp_id}/request", status_code=201)
async def create_request(
    emp_id: int,
    request_info: ChangeInfoRequestBody,
    employee_obj: Annotated[Employee, Depends(employee_factory)],
):
    try:
        if not employee_obj.emp_id == emp_id:
            raise ForbiddenErr(f"You can't create a request for employee id {emp_id}")
        else:
            request_id = await employee_obj.request_self_info_change(
                request_info.model_dump(), emp_id
            )
            return {"success": True, "request_id": request_id}
    except ForbiddenErr as err:
        raise ForbiddenErr(err.detail)
    except ValueError as err:
        raise InvalidValueErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del employee_obj


# not doneeee
@employee_router.get("/{emp_id}/request", status_code=200)
async def get_requests(
    emp_id: int,
    status: str | None,
    employee_obj: Annotated[Employee, Depends(employee_factory)],
):
    try:
        status_list = None
        if status:
            status_list = csv_to_list_of_alpha_num_str(status)
            status_list = [item for item in status_list if item in ]
            if len(status_list) == 0:
                raise InvalidValueErr("Request status query string is invalid")
        else:
            status_list = ["approved_by_hr","hr_assigned","committed","rejected"]

        data = await employee_obj.get_my_requests(status_list)
        return data
    except InvalidValueErr as err:
        raise InvalidValueErr(err.detail)
    except ValueError as err:
        raise NotFoundErr(err)
    except Exception as err:
        raise InternalServerErr(err)


@employee_router.get("/{emp_id}", status_code=200)
async def get_my_profile(employee):
    pass


def request_update_controler(employee, update_info):
    pass

import json

from typing import Annotated, final
from fastapi import APIRouter,Request, Depends, HTTPException
from pydantic import ValidationError
from ..utils.general_utils import csv_to_list

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
        new_employee: EmployeeInfo, request:Request
):
    admin_obj = request.state.user_obj
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
    request: Request
):
    baisc_employee_obj = request.state.user_obj
    try:
        pass
        data = await baisc_employee_obj.search_other_employee(query_username)
        for item in data:
            item["emp_id"] = item["empid"]
            del item["empid"]
        return {"success": True, "data": data}
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del baisc_employee_obj


@employee_router.delete("/{emp_id}", status_code=204)
async def remove_employee(
        emp_id: int, request: Request
):
    admin_obj = request.state.user_obj
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


@employee_router.post("/request", status_code=201)
async def create_request(
    request_info: ChangeInfoRequestBody,
    requst: Request
):
    employee_obj = requst.state.user_obj
    try:
        request_id = await employee_obj.request_self_info_change(
            request_info.model_dump(), employee_obj.emp_id
        )
        return {"success": True, "request_id": request_id}
    except ValueError as err:
        raise InvalidValueErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del employee_obj


@employee_router.get("/request", status_code=200)
async def get_my_requests(
    request: Request,
    status: str | None = None,
):
    employee_obj = request.state.user_obj
    try:
        status_list = None
        if status:
            status_list = csv_to_list(status)
            status_list = [
                item
                for item in status_list
                if item in ["approved_by_hr", "hr_assigned", "committed", "rejected"]
            ]
            if len(status_list) == 0:
                raise InvalidValueErr("Request status query string is invalid")
        else:
            status_list = ["approved_by_hr", "hr_assigned", "committed", "rejected"]

        data = await employee_obj.get_my_requests(status_list)
        return {"success": True, "data": data}
    except InvalidValueErr as err:
        raise InvalidValueErr(err.detail)
    except ValueError as err:
        raise NotFoundErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del employee_obj


@employee_router.get("/profile", status_code=200)
async def get_my_profile(request:Request):
    employee_obj = request.state.user_obj 
    try:
        profile_info = await employee_obj.get_profile_info()
        return {"success": True, "profile_info": profile_info}
    except ValueError as err:
        raise NotFoundErr(err)
    except Exception as err:
        raise InternalServerErr(err)

@employee_router.get("/{emp_id}/reports_to",status_code=200)
async def get_reports_to(emp_id:int,request:Request):
    worker_obj = request.state.user_obj
    try:
       data = await worker_obj.reports_to(emp_id)
       return {"success":True,"data":data}
    except ValueError as err:
       raise NotFoundErr(err)
    except Exception as e:
        raise InternalServerErr(e)
    finally:
        del worker_obj

def request_update_controler(employee, update_info):
    pass

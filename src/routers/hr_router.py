from fastapi import APIRouter, Request,Depends
from typing import Annotated
from ..factories import user_dependency
from ..entities.hr.hr_employee import Hr_employee
from ..utils.general_utils import csv_to_list
from ..execptions.HttpExceptions import InternalServerErr, InvalidValueErr, NotFoundErr
from ..types.general_types import UpdateReqStatusBodyHr

hr_router = APIRouter()

STATUS_VALID_VALUES = ["committed", "rejected", "approved_by_hr", "hr_assigned"]


@hr_router.get("/request", status_code=200)
async def get_requests_hr(hr_obj:Annotated[Hr_employee,Depends(user_dependency)],status: str):
    data = []
    try:
        status_list = csv_to_list(status)
        status_list = [
            status for status in status_list if status in STATUS_VALID_VALUES
        ]
        data = await hr_obj.get_assigned_requests_by_status(status_list)
        return {"success": True, "data": data}
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del hr_obj


@hr_router.patch("/request/{req_id}", status_code=204)
async def update_request_status_with_remark(
    req_id: int, req_body: UpdateReqStatusBodyHr, hr_obj:Annotated[Hr_employee,Depends(user_dependency)]
):
    try:
        status = (
            req_body.request_status
            if req_body.request_status in STATUS_VALID_VALUES
            else None
        )
        if not status:
            raise ValueError("Invalid status value")
        remark = req_body.remark
        data = []
        await hr_obj.update_request_status_with_remark(req_id, remark, status)
        return {"success": True, "data": data}
    except ValueError as err:
        if "not exsists" in str(err):
            raise NotFoundErr(err)
        else:
            raise InvalidValueErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del hr_obj

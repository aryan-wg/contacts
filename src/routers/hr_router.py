from fastapi import APIRouter, Request
from ..utils.general_utils import csv_to_list
from ..execptions.HttpExceptions import InternalServerErr, InvalidValueErr, NotFoundErr
from ..types.general_types import UpdateReqStatusBodyHr

hr_router = APIRouter()

STATUS_VALID_VALUES = ["committed", "rejected", "approved_by_hr", "hr_assigned"]


@hr_router.get("/request", status_code=200)
async def get_requests_hr(status: str, request: Request):
    hr_obj = request.state.user_obj
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
    req_id: int, req_body: UpdateReqStatusBodyHr, request: Request
):
    hr_obj = request.state.user_obj
    try:
        status = (
            req_body.request_status
            if req_body.request_status in STATUS_VALID_VALUES
            else None
        )
        if not status:
            raise ValueError("Invalid status value")
        remark = req_body.remak
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

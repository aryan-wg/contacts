from fastapi import APIRouter, Request, Path,Depends
from typing import Annotated
from ..factories import user_dependency
from ..utils.general_utils import csv_to_list
from ..execptions.HttpExceptions import InternalServerErr, InvalidValueErr, NotFoundErr
from ..entities.admin.admin import Admin
admin_router = APIRouter()

STATUS_VALID_VALUES = ["committed", "rejected", "approved_by_hr", "hr_assigned"]


@admin_router.get("/request", status_code=200)
async def get_requests_admin(admin_obj:Annotated[Admin,Depends(user_dependency)],status: str | None = None):
    # admin_obj = request.state.user_obj
    data = []
    try:
        if not status:
            status_list = STATUS_VALID_VALUES
        else:
            status_list = csv_to_list(status)
            status_list = [
                status for status in status_list if status in STATUS_VALID_VALUES
            ]
        data = await admin_obj.get_req(status_list)
        return {"success": True, "data": data}
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del admin_obj 


@admin_router.patch("/request/{req_id}", status_code=204)
async def update_request_status(
     admin_obj:Annotated[Admin,Depends(user_dependency)],req_id: int = Path(gt=0)
):
    try:
        data = []
        await admin_obj.commit_request(req_id)
        return {"success": True, "data": data}
    except ValueError as err:
        if "not exist" in str(err):
            raise NotFoundErr(err)
        else:
            raise InvalidValueErr(err)
    except Exception as err:
        raise InternalServerErr(err)
    finally:
        del admin_obj 

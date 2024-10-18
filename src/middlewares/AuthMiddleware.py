from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..factories import user_factory
from ..Logger.Logger import Logger
from ..types.general_types import LOG_LEVEL_ENUM
PATHS = {
    "/api/v1/employee/": {"GET": ["employee"], "POST": ["admin"]},
    "/api/v1/employee/profile/": {"GET": ["employee"]},
    "/api/v1/employee/request/": {"GET": ["employee"], "POST": ["employee"]},
    "/api/v1/employee/{emp_id}/reported_by/": {"GET": ["worker", "hr", "admin"]},
    "/api/v1/employee/{emp_id}/reports_to/": {
        "GET": ["worker", "hr", "admin"],
        "PUT": ["admin"],
    },
    "/api/v1/employee/{emp_id}/": {"DELETE": ["admin"]},
    "/api/v1/admin/request/{req_id}/": {"PATCH": ["admin"]},
    "/api/v1/admin/request/":{"GET": ["admin"]},
    "/api/v1/hr/request/": {"GET": ["hr"]},
    "/api/v1/hr/request/{req_id}/": {"PATCH": ["hr"]},
}


def check_if_matching(allowed_path_as_splitted_list, request_path_as_splitted_list):
    if not len(request_path_as_splitted_list) == len(allowed_path_as_splitted_list):
        return False
    for index in range(len(request_path_as_splitted_list)):
        if allowed_path_as_splitted_list[index] == request_path_as_splitted_list[
            index
        ] or (
            "{" in allowed_path_as_splitted_list[index]
            and "}" in allowed_path_as_splitted_list[index]
        ):
            continue
        else:
            return False
    else:
        return True


def get_path_pattern(path):
    request_path_as_splitted_list = path.split("/")
    request_path_as_splitted_list = [
        path for path in request_path_as_splitted_list if not path == ""
    ]
    all_allowed_paths_as_splitted_lists = [item.split("/") for item in PATHS.keys()]
    # print(request_path_as_splitted_list)
    # print(all_allowed_paths_as_splitted_lists)
    splitted = ""
    for allowed_path_as_splitted_list in all_allowed_paths_as_splitted_lists:
        allowed_path_as_splitted_list = [
            path for path in allowed_path_as_splitted_list if not path == ""
        ]
        if check_if_matching(
            allowed_path_as_splitted_list, request_path_as_splitted_list
        ):
            return "/"+"/".join(allowed_path_as_splitted_list)+"/"


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path_pattern = get_path_pattern(request.url.path)
        try:
            # path = request.url.path
            if path_pattern in PATHS.keys():
                allowed_user_types = PATHS[path_pattern][request.method]
                if not request.headers.get("authorization"):
                    raise HTTPException(status_code=401, detail="Auth token not found")
                else:
                    token = request.headers.get("authorization").split(" ")[1]
                    request.state.user_obj = user_factory(token, allowed_user_types,request.url.path)
                    response = await call_next(request)
                    return response
            else:
                return await call_next(request)
        except HTTPException as err:
            if err.status_code == 401:
                logger = Logger(log_file="logs.log",log_name="UNAUTHENTICATED")
                logger.log(f"{err.detail}",LOG_LEVEL_ENUM.INFO)
            elif err.status_code == 403:
                logger = Logger(log_file="logs.log",log_name="FORBIDDEN")
                logger.log(f"Path:{path_pattern}, {err.detail}",LOG_LEVEL_ENUM.ERROR)
            return JSONResponse(
                status_code=err.status_code,
                content={"success": False, "error": err.detail},
            )
        except Exception as err:
            return JSONResponse(
                status_code=401, content={"success": False, "error": str(err)}
            )

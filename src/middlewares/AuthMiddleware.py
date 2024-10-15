from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..execptions.HttpExceptions import UnauthorizedErr
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..factories import user_factory

PATHS = {
    "/api/v1/employee/": {"GET": ["employee"], "POST": ["admin"]},
    "/api/v1/employee/profile/": {"GET": ["employee"]},
    "/api/v1/employee/request/": {"GET": ["employee"], "POST": ["employee"]},
    "/api/v1/employee/{emp_id}/reported_by/": {"GET": ["worker","hr"]},
    "/api/v1/employee/{emp_id}/reports_to/": {"GET": ["worker","hr","admin"], "PUT": ["admin"]},
    "/api/v1/employee/{emp_id}/": {"DELETE": ["admin"]},
    "/api/v1/admin/request/": {"GET": ["admin"], "PATCH": ["admin"]},
    "/api/v1/hr/request/": {"GET": ["hr"], "PATCH": ["hr"]},
    "/api/v1/auth/employee/{emp_id}/password/": {"POST": ["employee"]},
}


def check_if_matching(allowed_path_as_splitted_list, request_path_as_splitted_list):
    for index in range(len(request_path_as_splitted_list)):
        if allowed_path_as_splitted_list[index] == request_path_as_splitted_list[index] \
            or ("{" in allowed_path_as_splitted_list[index] and "}" in allowed_path_as_splitted_list[index]):
            continue
        else: 
            return False
    else:
        return True


def get_path_pattern(path):
    request_path_as_splitted_list = path.split("/")
    all_allowed_paths_as_splitted_lists = [item.split("/") for item in PATHS.keys()]
    # print(request_path_as_splitted_list)
    # print(all_allowed_paths_as_splitted_lists)
    for allowed_path_as_splitted_list in all_allowed_paths_as_splitted_lists:
        if check_if_matching(allowed_path_as_splitted_list, request_path_as_splitted_list):
            return "/".join(allowed_path_as_splitted_list)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # path = request.url.path
            # print(request.method)
            # print(request.url.path)
            path_pattern = get_path_pattern(request.url.path)
            print("path pattern is ",path_pattern)
            if path_pattern in PATHS.keys():
                allowed_user_types = PATHS[path_pattern][request.method]
                token = request.headers.get("authorization").split(" ")[1]
                request.state.user_obj = user_factory(token, allowed_user_types)
                response = await call_next(request)
                return response
            else:
                return await call_next(request)
        except Exception as err:
            return JSONResponse(
                status_code=401, content={"success": False, "error": str(err)}
            )

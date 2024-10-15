from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..execptions.HttpExceptions import UnauthorizedErr
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..factories import user_factory
PATHS = {
    "/auth/employee/{emp_id}/password/": {"POST": ["employee"]},
    "/employee/": {"GET": ["employee"],"POST":["admin"]},
    "/employee/profile/": {"GET": ["employee"]},
    "/employee/request/": {"GET": ["employee"], "POST": ["employee"]},
    "/employee/{emp_id}/reported_by/": {"GET": ["employee"]},
    "/employee/{emp_id}/reports_to/": {"GET": ["employee"], "POST": ["admin"]},
    "/employee/{emp_id}/": {"DELETE": ["admin"]},
    "/admin/request/": {"GET": ["admin"], "PATCH": ["admin"]},
    "/hr/request/": {"GET": ["hr"], "PATCH": ["hr"]},
}

def get_path_pattern(path):
    split_path_list = path.split("/")
    assigned_paths = [item.split("/")]
    for item in split_path_list:

        if "{" in item

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # path = request.url.path 
            print(request.method)
            print(request.url.path)
            path_pattern = get_path_pattern(request.url.path)
            if path_pattern in PATHS.keys():
                allowed_user_types = PATHS[path_pattern][request.method]
                token = request.headers.get("authorization").split(" ")[1]
                request.state.user_obj = user_factory(token,allowed_user_types)
                response = await call_next(request)
                return response
            else:
                return await call_next(request)
        except Exception as err:
            return JSONResponse(status_code = 401 ,content = {"success":False,"error":str(err)})

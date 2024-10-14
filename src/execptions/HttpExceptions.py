from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class InternalServerErr(HTTPException):
    def __init__(self, errorInfo):
        super().__init__(status_code=500, detail=errorInfo)


class InvalidValueErr(HTTPException):
    def __init__(self, errorInfo):
        super().__init__(status_code=400, detail=errorInfo)


class NotFoundErr(HTTPException):
    def __init__(self, errorInfo):
        super().__init__(status_code=404, detail=errorInfo)

class NotAllowedErr(HTTPException):
    def __init__(self, errorInfo):
        super().__init__(status_code=405, detail=errorInfo)

class ForbiddenErr(HTTPException):
    def __init__(self,errorInfo):
        print(errorInfo)
        super().__init__(status_code=403,detail=errorInfo)

async def standard_err_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"success": False, "error": str(exception.detail)},
    )


async def pydantic_schema_err_handler(
    request: Request, exception: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": exception.errors()[0]["msg"]},
    )


exceptions = [
    (InternalServerErr, standard_err_handler),
    (InvalidValueErr, standard_err_handler),
    (NotFoundErr, standard_err_handler),
    (NotAllowedErr,standard_err_handler),
    (ForbiddenErr,standard_err_handler),
    (RequestValidationError, pydantic_schema_err_handler),

]

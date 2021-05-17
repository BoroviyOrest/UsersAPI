from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from db.exceptions import DatabaseResultException


async def database_result_error_handler(request: Request, exc: DatabaseResultException):
    return JSONResponse(
        status_code=404,
        content={
            'message': str(exc)
        }
    )


async def auth_jwt_error_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'message': exc.message
        }
    )

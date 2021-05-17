from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from api.api import api_router
from core.events import on_startup_handler, on_shutdown_handler
from core.exception_handlers import database_result_error_handler, auth_jwt_error_handler
from db.exceptions import DatabaseResultException
from models.settings import Settings


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler('startup', on_startup_handler(application))
    application.add_event_handler('shutdown', on_shutdown_handler(application))

    application.include_router(api_router)

    application.exception_handler(DatabaseResultException)(database_result_error_handler)
    application.exception_handler(AuthJWTException)(auth_jwt_error_handler)

    AuthJWT.load_config(lambda: Settings())

    return application


app = get_application()

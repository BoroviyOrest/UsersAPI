from fastapi import APIRouter

from api.endpoints import auth, user

api_router = APIRouter()

api_router.include_router(
    user.router,
    tags=['user'],
    prefix='/user'
)

api_router.include_router(
    auth.router,
    tags=['auth'],
    prefix='/auth'
)

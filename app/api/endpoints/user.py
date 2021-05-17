from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from core.dependencies import init_service
from models.user import UserInResponse, UserInUpdate
from services.user import UserService

router = APIRouter()


@router.get('/{user_id}', response_model=UserInResponse)
async def get_quiz_by_id(
        user_id: str,
        service: UserService = Depends(init_service(UserService)),
        authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    quiz = await service.get_by_id(user_id)

    return quiz


@router.get('/', response_model=list[UserInResponse])
async def get_all_quizzes(
        service: UserService = Depends(init_service(UserService)),
        authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    quizzes_list = await service.get_all()

    return quizzes_list


@router.put('/{user_id}', response_model=UserInResponse)
async def update_quiz(
        user_id: str,
        user_data: UserInUpdate,
        service: UserService = Depends(init_service(UserService)),
        authorize: AuthJWT = Depends()
):
    authorize.jwt_required()

    new_user = await service.update(user_id, user_data)

    return new_user

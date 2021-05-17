from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from core.dependencies import init_service
from models.user import UserInLogin, UserInCreate, UserInResponse
from services.user import UserService

router = APIRouter()


@router.post('/sign_up', response_model=UserInResponse, status_code=201)
async def get_quiz_by_id(user_data: UserInCreate, service: UserService = Depends(init_service(UserService))):
    user = await service.sign_up(user_data)

    return user


@router.post('/login')
async def login(
        user_data: UserInLogin,
        service: UserService = Depends(init_service(UserService)),
        authorize: AuthJWT = Depends()
):
    user = await service.check_login(user_data)
    claims = {
        'dtls': {
            'email': user.email,
            'is_active': user.is_active,
            'is_admin': user.is_admin,
        }
    }
    user_id_str = str(user.id)
    access_token = authorize.create_access_token(subject=user_id_str, user_claims=claims)
    refresh_token = authorize.create_refresh_token(subject=user_id_str, user_claims=claims)

    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/refresh')
async def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    custom_claims = {'dtls': authorize.get_raw_jwt()['dtls']}
    new_access_token = authorize.create_access_token(subject=current_user, user_claims=custom_claims)

    return {'access_token': new_access_token}

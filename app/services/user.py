from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from crud.user import UserCRUD
from db.exceptions import DatabaseResultException
from models.user import UserInCreate, UserInDB, UserInLogin, UserInUpdate
from core.security import get_password_hash, generate_salt, verify_password


class UserService:
    """"""

    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._user_crud = UserCRUD(client)

    async def get_by_id(self, user_id: str) -> UserInDB:
        """

        :param user_id:
        :return:
        """
        return await self._user_crud.get(_id=user_id)

    async def get_all(self) -> list[UserInDB]:
        """

        :return:
        """
        return await self._user_crud.get_many()

    async def sign_up(self, sign_up_data: UserInCreate) -> UserInDB:
        """

        :param sign_up_data:
        :return:
        """
        salt = generate_salt()
        hashed_password = get_password_hash(salt + sign_up_data.password)
        user_data = {
            'username': sign_up_data.username,
            'email': sign_up_data.email,
            'salt': salt,
            'hashed_password': hashed_password
        }

        return await self._user_crud.create(user_data)

    async def check_login(self, login_data: UserInLogin) -> UserInDB:
        """

        :param login_data:
        :return:
        """
        user = await self._user_crud.get(email=login_data.email)
        is_correct = verify_password(user.salt + login_data.password, user.hashed_password)
        if is_correct is False:
            raise

        return user

    async def update(self, user_id: str, user_data: UserInUpdate) -> UserInDB:
        """

        :param user_id:
        :param user_data:
        :return:
        """
        return await self._user_crud.update(user_id=ObjectId(user_id), user_data=user_data.dict())

    async def check_if_admin(self, user_id: str) -> bool:
        """

        :param user_id:
        :return:
        """
        try:
            await self._user_crud.get(_id=ObjectId(user_id), is_admin=True)
            return True
        except DatabaseResultException:
            return False

from bson import ObjectId
from pymongo import ReturnDocument

from crud.base import AbstractCRUD
from db.exceptions import DatabaseResultException
from models.user import UserInDB


class UserCRUD(AbstractCRUD):
    """"""

    _collection_name = 'users'
    _model = UserInDB

    async def create(self, user_data: dict) -> UserInDB:
        """

        :param user_data:
        :return:
        """
        check_duplicate = await self._db[self._collection_name].find_one({'email': user_data['email']})
        if check_duplicate is not None:
            raise DatabaseResultException(f'There is a user with email "{user_data["email"]}" already')

        await self._db[self._collection_name].insert_one(user_data)
        user = self._model(**user_data)

        return user

    async def update(self, user_id: ObjectId, user_data: dict) -> UserInDB:
        """
        Update user document in the DB by user _id
        :param user_id: should be valid ObjectId string
        :param user_data: quiz data in QuizInCreate format
        :return: UserInDB instance filled with quiz data
        """

        new_user = await self._db[self._collection_name].find_one_and_update(
            {'_id': user_id},
            {'$set': user_data},
            return_document=ReturnDocument.AFTER
        )
        if new_user is None:
            raise DatabaseResultException(f'There are no users with ObjectId("{user_data}")')

        return self._model(**new_user)

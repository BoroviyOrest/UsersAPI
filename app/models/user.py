from pydantic import BaseModel, EmailStr, validator

from models.db import DBModelMixin


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class BaseUserDetailed(BaseUser):
    is_active: bool = True
    is_admin: bool = False


class UserInDB(BaseUserDetailed, DBModelMixin):
    salt: str
    hashed_password: str


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str
    repeat_password: str

    @validator("password")
    def validate_password_length(cls, value, **kwargs):
        if len(value) < 6:
            raise ValueError("Password is too short.")
        return value

    @validator("repeat_password")
    def validate_passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match.")
        return value


class UserInUpdate(BaseModel):
    is_active: bool = True
    is_admin: bool = False


class UserInResponse(BaseUser):
    pass


class UserInResponseDetailed(BaseUserDetailed):
    pass

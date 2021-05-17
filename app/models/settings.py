from pydantic import BaseModel

from core.config import jwt_secret


class Settings(BaseModel):
    authjwt_secret_key: str = jwt_secret

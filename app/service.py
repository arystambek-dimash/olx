from datetime import datetime, timedelta
from typing import Optional, Dict
from pydantic import BaseModel, Field
from jose import jwt

from app.errors import InvalidToken
from app.auth.models.repository.repository import UserCRUD


# JWT Configuration
class JWTData(BaseModel):
    user_id: str = Field(alias="sub")


class JwtService:
    def __init__(
            self,
            algorithm: str,
            secret: str,
            expiration: timedelta,
    ) -> None:
        self.algorithm = algorithm
        self.secret = secret
        self.expiration = expiration

    def create_access_token(self, user_data: dict) -> str:
        expires_delta = timedelta(minutes=self.expiration)

        jwt_data = {
            "sub": str(user_data["id"]),
            "exp": datetime.utcnow() + expires_delta,
        }

        return jwt.encode(jwt_data, self.secret, algorithm=self.algorithm)

    def parse_jwt_user_data(self, token: str) -> Optional[JWTData]:
        if not token:
            return None

        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise InvalidToken()

        return JWTData(**payload)


##Initalization UserRepository and JWToken
class Service:
    def __init__(
            self,
            repository: UserCRUD,
            jwt_svc: JwtService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc

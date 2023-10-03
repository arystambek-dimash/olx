from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from config.database import SessionLocal
from config.settings import config

from app.service import JWTData, JwtService, Service
from app.errors import AuthenticationRequiredException
from app.auth.models.repository.repository import UserCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service():
    repository = UserCRUD()
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)

    svc = Service(repository, jwt_svc)
    return svc


def parse_jwt_user_data(
        token: str = Depends(oauth2_scheme),
        svc: Service = Depends(get_service),
) -> JWTData:
    token = svc.jwt_svc.parse_jwt_user_data(token)
    if not token:
        raise AuthenticationRequiredException

    return token

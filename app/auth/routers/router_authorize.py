from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from . import router, Session
from app.auth.utils.security import check_password
from app.dependencies import get_service, get_db
from app.service import Service

from pydantic import BaseModel


class AuthorizeUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/users/tokens", response_model=AuthorizeUserResponse)
async def authorize(
        input: OAuth2PasswordRequestForm = Depends(),
        svc: Service = Depends(get_service),
        db: Session = Depends(get_db)
):
    user = svc.repository.get_user_by_username(db, input.username)
    data = {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "last_name": user.last_name,
        "password": user.password
    }
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not user such username!")
    if not check_password(password=input.password, password_in_db=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Password incorrect or not user not found!")
    return AuthorizeUserResponse(
        access_token=svc.jwt_svc.create_access_token(user_data=data),
    )

from typing import Any

from fastapi import Depends
from pydantic import Field, BaseModel

from app.service import Service, JWTData
from app.dependencies import get_service, parse_jwt_user_data, get_db
from . import router, Session


class GetMyAccountResponse(BaseModel):
    id: Any = Field(alias="id")
    username: str
    name: str
    last_name: str


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
        db: Session = Depends(get_db)

) -> dict[str, str]:
    user = svc.repository.get_user_by_id(db, jwt_data.user_id)
    return user

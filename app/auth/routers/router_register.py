from fastapi import Depends, HTTPException, status
from app.dependencies import get_service, get_db
from app.service import Service
from app.auth.models.schemas import UserCreate, User

from . import router, Session


@router.post("/users", response_model=User)
def register(user: UserCreate, svc: Service = Depends(get_service), db: Session = Depends(get_db)):
    if svc.repository.get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already taken.")
    user_db = svc.repository.create_user(db, user)
    return user_db

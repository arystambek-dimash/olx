from app.auth.models.schemas import UserCreate
from ..models import User
from sqlalchemy.orm import Session
from app.auth.utils.security import hash_password


class UserCRUD:
    def create_user(self, db: Session, user: UserCreate) -> User:
        user_db = User(name=user.name, last_name=user.last_name, username=user.username,
                       password=hash_password(user.password))
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return user_db

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        """

        :rtype: object
        """
        user_db = db.query(User).filter(User.id == user_id).first()
        if user_db:
            return user_db
        return None

    def get_user_by_username(self, db: Session, username: str) -> User:
        user_db = db.query(User).filter(User.username == username).first()
        if user_db:
            return user_db
        return None

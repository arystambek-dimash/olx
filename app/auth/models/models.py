from config.database import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

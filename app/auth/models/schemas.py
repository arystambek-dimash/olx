from pydantic import BaseModel, Field, validator
import re


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    name: str = Field(max_length=40, min_length=2)
    last_name: str = Field(max_length=40, min_length=2)
    password: str

    @validator('password')
    def validate_password(cls, v):
        pattern = r"^^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                'Password must have at least one lowercase letter, one uppercase letter, one digit, one special character, and be between 8 to 30 characters long')
        return v


class User(UserBase):
    id: int

    class Config:
        from_attributes = True

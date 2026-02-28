from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
import re
from uuid import UUID

USERNAME_REGEX = re.compile(
    r"^(?=.{3,30}$)(?![._-])(?!.*[._-]{2})[a-zA-Z0-9._-]+(?<![._-])$"
)

class UserBase(BaseModel):
    username: str
    
    # Lanzar 422 si hay campos extra
    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    def validate_username(cls, v: str) -> str:
        if not USERNAME_REGEX.fullmatch(v):
            raise ValueError("Caracteres no permitidos")
        return v

class UserCreateRequest(UserBase):
    password: str

class UserCreateResponse(UserBase):
    id: UUID


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    password: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
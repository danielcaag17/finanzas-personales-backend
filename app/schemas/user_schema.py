from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
import re

class UserBase(BaseModel):
    username: str
    
    # Lanzar 422 si hay campos extra
    model_config = ConfigDict(extra="forbid")

    @field_validator("username")
    def no_html_tags(cls, v: str) -> str:
        if re.search(r"[<>]", v):
            raise ValueError("Caracteres no permitidos")
        return v

class UserCreateRequest(UserBase):
    password: str

class UserCreateResponse(UserBase):
    id: int


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    password: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
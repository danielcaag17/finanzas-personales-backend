from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(extra="forbid")

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
from app.repositories.user_repository import create_user_db, get_users_db
from app.database import get_db
from app.schemas.user_schema import UserCreateRequest, UserCreateResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.config.security import encrypt_password

router = APIRouter()

@router.post("", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreateRequest, db: Session = Depends(get_db)):
    data.password = encrypt_password(data.password)
    return create_user_db(db, data)

@router.get("", response_model=list[UserCreateResponse])
def get_users(db: Session = Depends(get_db)):
    return get_users_db(db)

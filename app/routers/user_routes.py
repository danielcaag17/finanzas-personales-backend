from app.repositories.user_repository import create_user_db, get_users_db
from app.database import get_db
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("", response_model=UserCreate)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user_db(db, data)

@router.get("", response_model=list[UserCreate])
def get_users(db: Session = Depends(get_db)):
    return get_users_db(db)

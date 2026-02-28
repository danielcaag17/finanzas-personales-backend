from app.models.user import User
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate


def create_user_db(db: Session, data: UserCreate) -> User:
    user_instace = User(**data.model_dump())
    db.add(user_instace)
    db.commit()
    db.refresh(user_instace)
    return user_instace

def get_users_db(db: Session) -> list[User]:
    return db.query(User).all()

def get_user_by_username_db(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()
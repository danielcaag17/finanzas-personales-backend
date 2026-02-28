from sqlalchemy import Column, String
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)

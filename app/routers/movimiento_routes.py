from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.movimiento_repository import create_movimiento_db
from app.schemas.movimiento_schema import MovimientoCreate, MovimientoCreateResponse, MovimientoCreateRequest
from app.deps import CurrentUser, get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

# Real path /api/users/{user_id}/movimientos
@router.post("", response_model=MovimientoCreateResponse, status_code=status.HTTP_201_CREATED)
def create_movimiento(data: MovimientoCreateRequest, user_id: str, authorization_user_id: CurrentUser, db: Session = Depends(get_db)):
    if user_id != str(authorization_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    movimiento_data = MovimientoCreate(**data.model_dump(), usuario_id=user_id)
    return create_movimiento_db(db, movimiento_data)
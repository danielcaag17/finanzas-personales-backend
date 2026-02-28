from app.models.movimiento import Movimiento
from sqlalchemy.orm import Session
from app.schemas.movimiento_schema import MovimientoCreate


def create_movimiento_db(db: Session, data: MovimientoCreate) -> Movimiento:
    movimiento_instance = Movimiento(**data.model_dump())
    db.add(movimiento_instance)
    db.commit()
    db.refresh(movimiento_instance)
    return movimiento_instance
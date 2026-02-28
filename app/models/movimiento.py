from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from app.database import Base

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, index=True)
    monto = Column(Integer, index=True)
    tipo_movimiento = Column(String, index=True)
    categoria = Column(String, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    cuenta_origen = Column(String, index=True)
    fecha = Column(String, index=True)

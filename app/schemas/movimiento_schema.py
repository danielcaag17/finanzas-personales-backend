from pydantic import BaseModel, ConfigDict, field_validator
import re
from datetime import date

class MovimientoBase(BaseModel):
    descripcion: str
    monto: int
    tipo_movimiento: str
    categoria: str
    cuenta_origen: str
    fecha: date | str

    model_config = ConfigDict(extra="forbid")

    @field_validator("descripcion", "cuenta_origen", "categoria", "tipo_movimiento", "fecha")
    def no_html_tags(cls, v: str) -> str:
        # rechaza si hay < o > en el string
        if re.search(r"[<>]", v):
            raise ValueError("Caracteres no permitidos")
        return v
    
    @field_validator("tipo_movimiento")
    def validar_tipo(cls, v):
        if v not in ["gasto fijo", "gasto variable", "ingreso"]:
            raise ValueError("Tipo de movimiento inválido")
        return v

class MovimientoCreateRequest(MovimientoBase):
    pass

class MovimientoCreate(MovimientoBase):
    usuario_id: int

class MovimientoCreateResponse(MovimientoBase):
    id: int
    usuario_id: int

class Movimiento(MovimientoBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)
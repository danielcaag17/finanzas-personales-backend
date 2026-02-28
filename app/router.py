from fastapi import APIRouter
from app.routers.user_routes import router as create_user
from app.routers.user_routes import router as get_users
from app.routers.movimiento_routes import router as create_movimiento

router = APIRouter()

# Registrar subrouters
router.include_router(create_user, prefix="/users", tags=["user"])
router.include_router(get_users, prefix="/users", tags=["user"])

router.include_router(create_movimiento, prefix="/movimientos", tags=["movimiento"])
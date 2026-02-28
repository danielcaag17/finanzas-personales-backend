from fastapi import APIRouter
from app.routers.user_routes import router as create_user
from app.routers.user_routes import router as get_users
from app.routers.movimiento_routes import router as create_movimiento
from app.routers.auth_routes import router as login_router

router = APIRouter()

# Registrar subrouters
router.include_router(login_router, prefix="/auth", tags=["auth"])

# Users
router.include_router(create_user, prefix="/users", tags=["user"])
router.include_router(get_users, prefix="/users", tags=["user"])

# Movimientos
router.include_router(create_movimiento, prefix="/movimientos", tags=["movimiento"])

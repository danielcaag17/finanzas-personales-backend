from fastapi import APIRouter

from app.routers.auth_routes import router as auth_router
from app.routers.user_routes import router as user_router
from app.routers.movimiento_routes import router as movimiento_router

router = APIRouter()

# Auth (público)
router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Users
router.include_router(user_router, prefix="/users", tags=["users"])

# Movimientos
router.include_router(
    movimiento_router,
    prefix="/users/{user_id}/movimientos",
    tags=["movimientos"]
)
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.router import router as api_router
from app.config.settings import settings
from app.config.cors import setup_cors
from app import models
from app.config.logging_config import setup_logging
import logging
from app.database import engine, Base

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación...")

    try:
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas: %s", list(Base.metadata.tables.keys()))
    except Exception:
        logger.exception("Error durante la inicialización de la base de datos")
        raise

    yield

    logger.info("Cerrando aplicación...")

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Proyecto inicial",
        version="0.0.1",
        lifespan=lifespan
    )

    setup_cors(app)
    setup_logging()
    app.include_router(api_router, prefix="/api")

    return app

app = create_application()

@app.get("/")
def read_root():
    return {"message": "Hola FastAPI"}


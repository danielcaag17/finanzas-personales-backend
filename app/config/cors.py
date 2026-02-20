from fastapi.middleware.cors import CORSMiddleware
from .settings import settings

def setup_cors(app):
    """
    Add middleware CORS optimized and secure
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "X-Api-Key"],
        expose_headers=["X-Total-Count"],
        max_age=600,  # Cache preflight for 10 min
    )
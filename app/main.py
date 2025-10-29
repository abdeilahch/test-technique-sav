from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import get_settings
from app.db.init_db import init_db
from app.api.tickets import router as tickets_router
from app.core.middleware import LoggingMiddleware
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="API de gestion de tickets",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.add_middleware(LoggingMiddleware)
    app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
    return app

app = create_app()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

Base = declarative_base()

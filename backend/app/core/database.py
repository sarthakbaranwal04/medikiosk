"""
SQLAlchemy engine, session factory, and declarative base.

Models (added in later phases) should inherit from `Base`.
Routers/services should depend on `get_db` to obtain a request-scoped session.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


def get_db() -> Generator:
    """FastAPI dependency that yields a database session and guarantees it's closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

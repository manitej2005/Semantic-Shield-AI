"""
Database connection pool lifecycle and session management for SemanticShield AI.
Supports dual-engine setups (SQLite for dev/local, PostgreSQL for production).
"""

import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.services.storage.models import Base

logger = logging.getLogger("app.services.storage.db")

# Configure connection parameters based on engine type
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Initializes database schema tables if they do not already exist.
    """
    try:
        logger.info(f"[Storage DB] Initializing tables for database URL: {settings.DATABASE_URL.split('@')[-1]}")
        Base.metadata.create_all(bind=engine)
        logger.info("[Storage DB] Database schema verified & initialized successfully.")
    except Exception as exc:
        logger.error(f"[Storage DB] Database initialization failed: {exc}", exc_info=True)
        raise exc


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency generator yielding a relational database session.
    Automatically handles session closing and cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI endpoint dependency wrapper for database session.
    """
    return get_db_session()

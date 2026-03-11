"""Database configuration and dependency provider.

This module creates an SQLAlchemy engine based on the
``DATABASE_URL`` environment variable and exposes ``get_db`` which is used
as a dependency in FastAPI endpoints to obtain a session. The session is
closed automatically when the request ends.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
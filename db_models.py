from sqlalchemy import Column, String, Float, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Db_Users(Base):
    """ORM model representing a registered user."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # record when the row was created; UTC timezone assumed by application
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Db_Expenses(Base):
    """ORM model for an expense entry tied to a user."""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    category = Column(String)  # stored as string, validated by Pydantic layer
    description = Column(String)
    date = Column(Date)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date as Date
from enum import Enum
from typing import Optional, List

class Category(str, Enum):
    """Allowed expense categories visible to the API."""
    groceries = "Groceries"
    leisure = "Leisure"
    electronics = "Electronics"
    utilities = "Utilities"
    clothing = "Clothing"
    health = "Health"
    others = "Others"

class ExpenseFilter(str, Enum):
    """Pre-defined range filters that can be passed to the list API.

    Aligned with the query logic in :pyfunc:`main.get_all`.
    """
    week = "week"
    month = "month"
    three_months = "3months"

class Token(BaseModel):
    """Response payload returned after a successful login."""
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    """Schema for returning user information to clients.

    ``from_attributes`` is enabled so that ORM objects can be returned directly.
    """
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    """Schema used when a client registers a new account."""
    email: str
    password: str

class ExpenseCreate(BaseModel):
    """Payload sent by clients when creating an expense entry."""
    amount: float
    category: Category
    description: str
    date: Date

class ExpenseUpdate(BaseModel):
    """Partial update model; all fields are optional."""
    amount: Optional[float] = None
    category: Optional[Category] = None
    description: Optional[str] = None
    date: Optional[Date] = None

class ExpenseResponse(BaseModel):
    """Schema returned by the API when an expense is retrieved."""
    id: int
    amount: float
    category: Category
    description: str
    date: Date
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ExpensePagination(BaseModel):
    page: int
    size: int
    total: int
    total_pages: int
    data: List[ExpenseResponse]
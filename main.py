from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
from models import UserCreate, ExpenseCreate, ExpenseUpdate, ExpenseResponse, Token, ExpenseFilter, ExpensePagination
from db_models import Db_Expenses, Db_Users, Base
from auth import hash_password, verify_password, create_access_token,get_current_user
from datetime import datetime, timedelta, timezone
from typing import Optional
from math import ceil

# FastAPI application instance
app = FastAPI()

# CORS middleware to allow requests from the frontend (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database tables based on the declarative models
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["health"])
def check():
    """Health check endpoint.

    Returns a simple message to verify the server is running.
    """
    return {"message": "Server is running"}


@app.post("/user/auth/signup", status_code=201, tags=["auth"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user.

    The password is hashed using bcrypt and the record is stored in the
    users table. If the email already exists, a 400 error is returned.
    """
    existing_user = db.query(Db_Users).filter(Db_Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    password_hashed = hash_password(user.password)
    new_user = Db_Users(email=user.email, password_hash=password_hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # returning basic feedback instead of full user object for security
    return {"message": "New user created", "user_id": new_user.id}


@app.post("/user/auth/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token.

    The OAuth2PasswordRequestForm expects fields "username" (email) and
    "password". If authentication succeeds a token is returned.
    """
    db_user = db.query(Db_Users).filter(Db_Users.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        # generic message to avoid leaking which part failed
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/user/expenses", response_model=ExpensePagination, tags=["expenses"])
def get_all(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    expense_filter: Optional[ExpenseFilter] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Db_Users = Depends(get_current_user),
):
    """Retrieve expenses belonging to the current user.

    Filtering options:
    * ``expense_filter`` can be ``week``, ``month`` or ``3months``.
    * ``start_date`` and ``end_date`` for arbitrary ranges (takes precedence
      over the enum filter if both are provided).
    """
    query = db.query(Db_Expenses).filter(Db_Expenses.user_id == current_user.id).order_by(Db_Expenses.created_at.desc())
    now = datetime.now(timezone.utc)

    # explicit date range overrides the enum filter if both are provided
    if start_date and end_date:
        query = query.filter(Db_Expenses.date >= start_date, Db_Expenses.date <= end_date)
    elif expense_filter == ExpenseFilter.week:
        query = query.filter(Db_Expenses.date >= now - timedelta(days=7))
    elif expense_filter == ExpenseFilter.month:
        query = query.filter(Db_Expenses.date >= now - timedelta(days=30))
    elif expense_filter == ExpenseFilter.three_months:
        query = query.filter(Db_Expenses.date >= now - timedelta(days=90))

    total = query.count()

    offset = (page - 1) * size

    expenses = query.offset(offset).limit(size).all()

    total_pages = ceil(total / size)

    return {
    "page": page,
    "size": size,
    "total": total,
    "total_pages": total_pages,
    "data": expenses
    }


@app.get("/user/expenses/{id}", response_model=ExpenseResponse, tags=["expenses"])
def get_expense(id: int, db: Session = Depends(get_db), current_user: Db_Users = Depends(get_current_user)):
    """Return a single expense by id, ensuring it belongs to the current user."""
    expense = (
        db.query(Db_Expenses)
        .filter(Db_Expenses.id == id, Db_Expenses.user_id == current_user.id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.post("/user/expenses", response_model=ExpenseResponse, status_code=201, tags=["expenses"])
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: Db_Users = Depends(get_current_user),
):
    """Create an expense record for the authenticated user."""
    new_expense = Db_Expenses(
        user_id=current_user.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@app.put("/user/expenses/{id}", response_model=ExpenseResponse, tags=["expenses"])
def update_expense(
    id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: Db_Users = Depends(get_current_user),
):
    """Partially update an existing expense belonging to the current user.

    Only fields provided in the request body will be changed.
    """
    existing = (
        db.query(Db_Expenses)
        .filter(Db_Expenses.user_id == current_user.id, Db_Expenses.id == id)
        .first()
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    if expense.amount is not None:
        existing.amount = expense.amount
    if expense.category is not None:
        existing.category = expense.category
    if expense.description is not None:
        existing.description = expense.description
    if expense.date is not None:
        existing.date = expense.date

    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/user/expenses/{id}", tags=["expenses"])
def delete_expense(
    id: int, db: Session = Depends(get_db), current_user: Db_Users = Depends(get_current_user)
):
    """Remove a specific expense for the logged-in user."""
    expense = (
        db.query(Db_Expenses)
        .filter(Db_Expenses.user_id == current_user.id, Db_Expenses.id == id)
        .first()
    )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
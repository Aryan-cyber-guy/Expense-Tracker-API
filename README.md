# Expense Tracker API

A RESTful expense tracking API built with **FastAPI** and **SQLAlchemy**, featuring JWT authentication and a fully self-contained frontend (Spendly). Users can register, log in, and manage their personal expenses with filtering, pagination, and category support.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [API Reference](#api-reference)
  - [Health Check](#health-check)
  - [Authentication](#authentication)
  - [Expenses](#expenses)
- [Expense Categories](#expense-categories)
- [Frontend](#frontend)
- [Running Tests](#running-tests)

---

## Features

- User registration and login with **bcrypt** password hashing
- **JWT-based** authentication (Bearer tokens, 60-minute expiry)
- Full **CRUD** operations for expense entries
- Filtering by predefined ranges (`week`, `month`, `3months`) or custom date ranges
- **Paginated** expense listing with configurable page size
- Enum-validated expense categories
- CORS enabled for frontend integration
- Auto-creates database tables on startup

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Framework  | FastAPI 0.135                     |
| ORM        | SQLAlchemy 2.0                    |
| Database   | PostgreSQL (via `psycopg2-binary`) |
| Auth       | `python-jose` (JWT) + `passlib` (bcrypt) |
| Validation | Pydantic v2                       |
| Server     | Uvicorn                           |
| Frontend   | Vanilla HTML/CSS/JS (Spendly UI)  |

---

## Project Structure

```
expense-tracker-api/
├── main.py           # FastAPI app, all route definitions
├── auth.py           # JWT creation, password hashing, auth dependency
├── database.py       # SQLAlchemy engine and session setup
├── db_models.py      # ORM table models (Db_Users, Db_Expenses)
├── models.py         # Pydantic request/response schemas and enums
├── index.html        # Spendly — self-contained frontend
└── requirements.txt  # Python dependencies
```

---

## Getting Started

You can try the project directly here:
https://aryan-cyber-guy.github.io/Expense-Tracker-API

Or follow the steps below to run it locally on your machine.

### Prerequisites

- Python 3.9+
- A running PostgreSQL instance

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/expense-tracker-api.git
   cd expense-tracker-api
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root with the following keys:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/expense_db
```

| Variable       | Description                                      |
|----------------|--------------------------------------------------|
| `SECRET_KEY`   | Secret used to sign and verify JWTs              |
| `DATABASE_URL` | SQLAlchemy-compatible PostgreSQL connection URL  |

### Running the Server

```bash
python main.py
```

Or with Uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs (Swagger UI) are at `http://localhost:8000/docs`.

---

## API Reference

### Health Check

| Method | Endpoint | Auth | Description        |
|--------|----------|------|--------------------|
| GET    | `/`      | No   | Server health check |

**Response**
```json
{ "message": "Server is running" }
```

---

### Authentication

#### Sign Up

`POST /user/auth/signup`

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response** `201 Created`
```json
{ "message": "New user created", "user_id": 1 }
```

---

#### Log In

`POST /user/auth/login`

Accepts `application/x-www-form-urlencoded` (OAuth2 password flow). Use `username` for the email field.

**Request Form Fields**
```
username=user@example.com
password=yourpassword
```

**Response** `200 OK`
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

All subsequent requests must include this token in the `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

---

### Expenses

All expense endpoints require a valid JWT token.

#### List Expenses

`GET /user/expenses`

**Query Parameters**

| Parameter        | Type     | Default | Description                                          |
|------------------|----------|---------|------------------------------------------------------|
| `page`           | int      | `1`     | Page number (≥ 1)                                    |
| `size`           | int      | `10`    | Items per page (1–100)                               |
| `expense_filter` | string   | —       | Predefined range: `week`, `month`, or `3months`      |
| `start_date`     | datetime | —       | Custom range start (overrides `expense_filter`)      |
| `end_date`       | datetime | —       | Custom range end (overrides `expense_filter`)        |

**Response** `200 OK`
```json
{
  "page": 1,
  "size": 10,
  "total": 42,
  "total_pages": 5,
  "data": [ { ...expense }, ... ]
}
```

---

#### Get Single Expense

`GET /user/expenses/{id}`

**Response** `200 OK`
```json
{
  "id": 1,
  "amount": 49.99,
  "category": "Groceries",
  "description": "Weekly groceries",
  "date": "2025-05-20",
  "created_at": "2025-05-20T10:30:00"
}
```

---

#### Create Expense

`POST /user/expenses`

**Request Body**
```json
{
  "amount": 49.99,
  "category": "Groceries",
  "description": "Weekly groceries",
  "date": "2025-05-20"
}
```

**Response** `201 Created` — returns the created expense object.

---

#### Update Expense

`PUT /user/expenses/{id}`

All fields are optional; only provided fields are updated.

**Request Body**
```json
{
  "amount": 59.99,
  "description": "Updated description"
}
```

**Response** `200 OK` — returns the updated expense object.

---

#### Delete Expense

`DELETE /user/expenses/{id}`

**Response** `200 OK`
```json
{ "message": "Expense deleted successfully" }
```

---

## Expense Categories

The `category` field accepts one of the following values:

| Value         |
|---------------|
| `Groceries`   |
| `Leisure`     |
| `Electronics` |
| `Utilities`   |
| `Clothing`    |
| `Health`      |
| `Others`      |

---

## Frontend

The project includes `index.html` — a self-contained frontend called **Spendly**. Open it in any browser and point it to your running API instance (edit the `API` constant at the top of the script block to match your server URL).

Features of the UI:
- Sign up / log in with tab-based switching
- Add, edit, and delete expenses via a modal
- Filter by week, month, 3 months, or a custom date range
- Paginated table with adjustable page size
- Keyboard shortcuts: `Esc` to close modals, `Enter` to submit, `←` / `→` to navigate pages

---

## Running Tests

The project uses **pytest**. To run the test suite:

```bash
pytest
```

> Test files should follow the `test_*.py` naming convention and be placed in a `tests/` directory or the project root.

<h1 align="center">💰 Expense Tracker API</h1>

<p align="center">
A robust and scalable RESTful API built with <b>FastAPI</b> that enables users to securely track, manage, and analyze their expenses.
</p>

<hr>

<h2>📌 Project Overview</h2>

<p>
This project is a backend system for an expense tracking application, designed with clean architecture and best practices in mind.
It allows users to register, authenticate, and efficiently manage their personal financial data.
</p>

<p>
The project demonstrates key backend engineering concepts such as:
</p>

<ul>
<li>RESTful API design and development</li>
<li>JWT-based authentication and authorization</li>
<li>Database management using SQLAlchemy ORM</li>
<li>Secure password hashing and data protection</li>
<li>Efficient data handling with filtering and pagination</li>
<li>Structured and maintainable backend architecture</li>
</ul>

<hr>

<h2>🚀 Features</h2>

<ul>
<li>👤 User Registration</li>
<li>🔐 JWT-based Authentication (Secure Login System)</li>
<li>💸 Full CRUD Operations for Expense Management (Create, Read, Update, Delete)</li>
<li>🔍 Advanced Filtering System (by date, category, etc.)</li>
<li>📄 Pagination Support for Efficient Data Retrieval</li>
<li>🛡 Secure Password Hashing using industry standards</li>
<li>📦 Database Integration with SQLAlchemy ORM</li>
<li>📚 Interactive API Documentation via Swagger (OpenAPI)</li>
</ul>

<hr>

<h2>🛠 Tech Stack</h2>

<ul>
<li><b>Backend:</b> FastAPI</li>
<li><b>Language:</b> Python</li>
<li><b>Database:</b> PostgreSQL / SQLite</li>
<li><b>ORM:</b> SQLAlchemy</li>
<li><b>Authentication:</b> JWT (JSON Web Token)</li>
<li><b>Validation:</b> Pydantic</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
Expense-Tracker-API
│
├── main.py              # Entry point of the application
├── models.py            # Pydantic schemas (request/response models)
├── db_models.py         # SQLAlchemy database models
├── database.py          # Database connection and session handling
├── auth.py              # Authentication logic (JWT, password hashing)
├── index.html           # Optional frontend/testing interface
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
</pre>

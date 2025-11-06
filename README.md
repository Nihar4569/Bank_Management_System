# 🏦 Banking Management System (BMS)

### A Modular Flask-based API for Account Management, Email Notifications, Batch Processing, and Web Scraping

---

## 📘 Overview

The **Banking Management System (BMS)** is a production-grade, multi-module Python **Flask API** that manages bank account records and supports advanced features such as automated email notifications, multithreaded balance computations, and web scraping for financial metadata.

It demonstrates clean architecture, asynchronous/batch processing, structured logging, and robust exception handling — all built with **PEP 8** compliance and **pytest** test coverage.

---

## 🚀 Key Features

✅ **CRUD REST API** — Manage `Account` entities (`id`, `name`, `number`, `balance`)
✅ **SQLite Database** — Persistent data storage via SQLAlchemy ORM
✅ **Email Notifications** — Automatic email when a new account is created
✅ **Batch Processing** — Multi-threaded or async total-balance calculations
✅ **Web Scraping** — Fetch interest rates or external bank info
✅ **Structured Logging** — JSON-ready, centralized logging setup
✅ **Error Handling** — Custom exceptions with unified handler
✅ **Testing Suite** — `pytest`-based unit tests for core modules
✅ **CLI Client** — Demonstration command-line client for testing API
✅ **PEP 8 Compliant** — Code style enforced via `flake8` or `pylint`

---

## 🧱 Architecture

```text
+----------------+        +-------------------------+       +------------------+
| Client (CLI)    | <----> |  Flask API Server         | <--> | SQLite Database  |
| or Postman      |        |  - CRUD Endpoints        |       | db.sqlite        |
|                 |        |  - Email Notification    |       +------------------+
|                 |        |  - Batch Calculation     |
|                 |        |  - Web Scraping Module   |
+----------------+         +-------------------------+
                                   |
                                   +--> SMTP / Mailtrap
```

---

## 📂 Project Structure

```bash
bms/
├── app/
│   ├── __init__.py        # Flask app factory
│   ├── config.py          # Configurations (DB URL, SMTP, batch size, etc.)
│   ├── models.py          # SQLAlchemy Account model
│   ├── db.py              # DB engine & session management
│   ├── crud.py            # CRUD operations
│   ├── routes.py          # API routes (Flask blueprints)
│   ├── emailer.py         # Email sending (sync & background)
│   ├── batch_calc.py      # Batch balance computation (threaded / async)
│   ├── scraper.py         # Web scraping utilities (interest rates)
│   ├── logger.py          # Structured logger setup
│   └── exceptions.py      # Custom exception classes
├── client/
│   └── cli.py             # CLI client to interact with API
├── tests/
│   ├── test_crud.py
│   └── test_batch_calc.py
├── run.py                 # App entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/bms.git
cd bms
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Edit or create `.env` file (optional):

```env
FLASK_ENV=development
DATABASE_URL=sqlite:///db.sqlite
SMTP_SERVER=smtp.mailtrap.io
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
OWNER_EMAIL=owner@example.com
BATCH_SIZE=10
```

### 5. Initialize Database

```bash
python
>>> from app.db import init_db
>>> init_db()
```

### 6. Run the Server

```bash
python run.py
```

Visit the API docs (if using `flasgger` or `swagger-ui`) at:

> [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 📡 API Endpoints

| Method | Endpoint         | Description                        |
| ------ | ---------------- | ---------------------------------- |
| GET    | `/accounts`      | List all accounts                  |
| GET    | `/accounts/<id>` | Retrieve single account            |
| POST   | `/accounts`      | Create a new account (sends email) |
| PUT    | `/accounts/<id>` | Update an existing account         |
| DELETE | `/accounts/<id>` | Delete an account                  |
| GET    | `/batch/total`   | Run batch balance calculation      |
| GET    | `/scraper/rates` | Fetch current interest rates       |

---

## 💌 Email Notification

When a new account is created, the system automatically sends a notification email to the configured `OWNER_EMAIL`.
This is handled by `emailer.py`, which can run as:

* A **background thread** using `ThreadPoolExecutor`
* Or asynchronously with `asyncio`

---

## ⚡ Batch Processing

The batch processor (`batch_calc.py`) computes **total balances** across all accounts in parallel:

* `ThreadPoolExecutor` (multi-threading)
* `asyncio.gather()` (coroutine-based)

You can specify the batch size in `config.py` or via environment variable.

---

## 🌐 Web Scraping Module

The **scraper** module uses `requests` + `BeautifulSoup` to fetch interest rates or public banking metadata (e.g., from central bank websites).
Optionally extendable with `selenium` for JS-heavy sites.

---

## 🧰 Testing

Run the full test suite:

```bash
pytest -v
```

Optional with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## 🧾 Logging

Structured logging is configured in `logger.py`:

* Console and file handlers
* JSON-ready output format
* Log rotation supported via `RotatingFileHandler`

Sample log format:

```json
{
  "timestamp": "2025-11-06T12:00:00Z",
  "level": "INFO",
  "module": "routes",
  "message": "Account created successfully"
}
```

---

## 🧑‍💻 CLI Client

A lightweight CLI (`client/cli.py`) interacts with the running API:

```bash
python client/cli.py create "John Doe" "123456789" 1000.0
python client/cli.py list
python client/cli.py total
```

---

## 🧩 Tech Stack

| Category     | Technology                    |
| ------------ | ----------------------------- |
| Framework    | Flask                         |
| ORM          | SQLAlchemy                    |
| Database     | SQLite                        |
| Async        | concurrent.futures / asyncio  |
| Web Scraping | Requests, BeautifulSoup       |
| Testing      | pytest                        |
| Logging      | Python `logging` (structured) |
| Email        | smtplib / mailtrap.io         |
| Style        | PEP 8, flake8, pylint         |

---

## 🧠 Future Enhancements

* JWT-based authentication
* Swagger / OpenAPI documentation
* Docker containerization
* Caching layer (Redis) for batch results
* Celery integration for background jobs

---

## 👨‍💻 Author

**Your Name**
📧 [your.email@example.com](mailto:your.email@example.com)
🔗 [GitHub](https://github.com/yourusername)

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to modify and distribute it.

---

Would you like me to include **badges** (build, coverage, license, etc.) or **example JSON requests/responses** in the README to make it more GitHub-ready?

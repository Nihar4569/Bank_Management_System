# 🏦 Banking Management System (BMS) — Docstring Reference

This document provides an overview of all modules and functions in the BMS Flask application, along with their purpose and parameters.  
Each function includes a **Python docstring-style description**.

---

## 📁 Module: `app/__init__.py`

### `create_app()`
```python
def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask app instance.
    """
````

---

## 📁 Module: `app/config.py`

### `Config`

```python
class Config:
    """
    Configuration class for Flask application.
    
    Attributes:
        SQLALCHEMY_DATABASE_URI (str): SQLite database file path.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable modification tracking.
        BATCH_SIZE (int): Default batch size for balance calculations.
        LOG_FILE (str): Path to log file for application logs.
    """
```

---

## 📁 Module: `app/db.py`

### `init_db(app)`

```python
def init_db(app):
    """
    Initialize database with Flask app context.
    
    Args:
        app (Flask): The Flask app instance.
    """
```

### `get_db_session()`

```python
def get_db_session():
    """
    Create and return a new SQLAlchemy database session.
    
    Returns:
        Session: SQLAlchemy session instance.
    """
```

---

## 📁 Module: `app/models.py`

### `class Account(db.Model)`

```python
class Account(db.Model):
    """
    Represents a bank account entity.

    Attributes:
        id (int): Primary key (auto-increment).
        name (str): Account holder’s name.
        number (str): Account number (unique).
        email (str): Registered user email.
        balance (float): Current account balance.
    """
```

---

## 📁 Module: `app/crud.py`

### `create_account(name, number, balance, email)`

```python
def create_account(name, number, balance, email):
    """
    Create a new bank account and send an email notification.

    Args:
        name (str): Account holder's name.
        number (str): Account number.
        balance (float): Initial deposit.
        email (str): Account holder’s email.

    Returns:
        Account: Created account instance.
    """
```

### `get_all_accounts()`

```python
def get_all_accounts():
    """Return all accounts stored in the database."""
```

### `get_account_by_id(account_id)`

```python
def get_account_by_id(account_id):
    """
    Retrieve an account by its ID.
    
    Args:
        account_id (int): Account ID.

    Returns:
        Account: Account object or None if not found.
    """
```

### `update_account(account_id, name=None, number=None, balance=None)`

```python
def update_account(account_id, name=None, number=None, balance=None):
    """
    Update existing account details and notify user via email.
    
    Args:
        account_id (int): Account ID.
        name (str, optional): Updated name.
        number (str, optional): Updated account number.
        balance (float, optional): Updated balance.
    """
```

### `delete_account(account_id)`

```python
def delete_account(account_id):
    """
    Delete an account and send a notification email.

    Args:
        account_id (int): Account ID.

    Returns:
        bool: True if successful, False otherwise.
    """
```

### `deposit_money(account_number, amount)`

```python
def deposit_money(account_number, amount):
    """
    Deposit money into an account.

    Args:
        account_number (str): Account number.
        amount (float): Deposit amount.
    """
```

### `withdraw_money(account_number, amount)`

```python
def withdraw_money(account_number, amount):
    """
    Withdraw money from an account if sufficient balance exists.

    Args:
        account_number (str): Account number.
        amount (float): Amount to withdraw.
    """
```

### `transfer_money(sender_number, receiver_number, amount)`

```python
def transfer_money(sender_number, receiver_number, amount):
    """
    Transfer money between two accounts.

    Args:
        sender_number (str): Sender's account number.
        receiver_number (str): Receiver's account number.
        amount (float): Amount to transfer.
    """
```

### `batch_calc()`

```python
def batch_calc():
    """
    Compute total, average, and count of balances across all accounts.
    
    Returns:
        dict: {"total_accounts", "total_balance", "average_balance"}
    """
```

---

## 📁 Module: `app/batch_calc.py`

### `calc_total_balance()`

```python
def calc_total_balance():
    """
    Calculate total account balances using ThreadPoolExecutor.

    Divides all account balances into index-based batches and sums concurrently.
    
    Returns:
        float: Total balance across all accounts.
    """
```

---

## 📁 Module: `app/email_utils.py`

### `send_mail(to_address, subject, body, attachment_path=None)`

```python
def send_mail(to_address, subject, body, attachment_path=None):
    """
    Send an email with optional file attachment using Gmail SMTP.

    Args:
        to_address (str): Receiver's email.
        subject (str): Email subject.
        body (str): Message text.
        attachment_path (str, optional): File path for attachment.

    Returns:
        bool: True if email sent successfully, else False.
    """
```

---

## 📁 Module: `app/scraper.py`

### `scrape_interest_rates()`

```python
def scrape_interest_rates():
    """
    Fetch interest rate information from multiple bank websites concurrently.

    Returns:
        list: List of dicts with {bank, url, info}.
    """
```

### `scrape_bank_names()`

```python
def scrape_bank_names():
    """
    Scrape list of bank names from RBI official website.

    Returns:
        list: List of bank names (strings).
    """
```

---

## 📁 Module: `app/exceptions.py`

### `class AppError(Exception)`

```python
class AppError(Exception):
    """Base class for all custom exceptions in the BMS system."""
```

### `class AccountNotFound(AppError)`

```python
class AccountNotFound(AppError):
    """Raised when a requested account does not exist."""
```

### `class InsufficientFunds(AppError)`

```python
class InsufficientFunds(AppError):
    """Raised when account has insufficient balance for a transaction."""
```

### `class InvalidTransaction(AppError)`

```python
class InvalidTransaction(AppError):
    """Raised when transaction input data is invalid."""
```

---

## 📁 Module: `app/logger.py`

### `logger`

```python
"""
Configured application logger instance for structured file-based logging.

Features:
- Logs INFO, WARNING, and ERROR messages
- Timestamped, formatted logs written to file 'bms.log'
"""
```

---

## 📁 Module: `app/routes.py`

```python
"""
Defines all RESTful API routes for account management, transactions,
batch balance calculation, and web scraping endpoints.

Endpoints:
    /accounts                → CRUD operations
    /accounts/deposit        → Deposit money
    /accounts/withdraw       → Withdraw money
    /accounts/transfer       → Transfer between accounts
    /batch_calc              → Total balance summary
    /scrape/interest-rates   → Scrape interest rate info
    /scrape/bank-names       → Scrape bank name list
"""

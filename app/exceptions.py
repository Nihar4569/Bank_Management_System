# app/exceptions.py
from flask import jsonify
from app.logger import logger


# ---------------------------
# 1️⃣ Custom Exception Classes
# ---------------------------

class BMSException(Exception):
    """Base class for all custom Banking Management System exceptions."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}


class AccountNotFoundError(BMSException):
    """Raised when an account cannot be found."""
    def __init__(self, account_id_or_number):
        super().__init__(f"Account not found: {account_id_or_number}", status_code=404)


class InsufficientFundsError(BMSException):
    """Raised when balance is insufficient for withdrawal or transfer."""
    def __init__(self, account_number):
        super().__init__(f"Insufficient balance in account {account_number}", status_code=400)


class InvalidTransferError(BMSException):
    """Raised when sender or receiver account number is invalid."""
    def __init__(self):
        super().__init__("Invalid sender or receiver account number", status_code=400)


# ---------------------------
# 2️⃣ Centralized Error Handler
# ---------------------------

def handle_bms_exception(error):
    """Handle all custom exceptions and return JSON + log it."""
    logger.error(f"{error.__class__.__name__}: {error.message}")
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def handle_generic_exception(error):
    """Handle any unexpected error."""
    logger.exception(f"Unexpected error: {error}")
    response = jsonify({"error": "An unexpected error occurred. Please try again later."})
    response.status_code = 500
    return response

from app.models import Account
from app.db import db
from app.logger import logger
from app.email_utils import send_mail   # ✅ Email sender
from app.exceptions import AccountNotFoundError, InsufficientFundsError, InvalidTransferError, BMSException


# ---------------- CREATE ----------------
def create_account(name, number, balance, email):
    """Create a new account and send confirmation email."""
    try:
        account = Account(name=name, number=number, balance=balance, email=email)
        db.session.add(account)
        db.session.commit()

        message = f"""
✅ New Account Created
-------------------------
Name: {name}
Account Number: {number}
Opening Balance: {balance}
"""
        send_mail(email, "Welcome! Your Account Has Been Created", message, None)
        logger.info(message.strip())
        return account

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error creating account {number}: {e}")
        raise BMSException("Failed to create account. Please try again.")


# ---------------- READ -----------------
def get_all_accounts():
    """Return all accounts."""
    return Account.query.all()


def get_account_by_id(account_id):
    """Return a single account by ID."""
    account = Account.query.get(account_id)
    if not account:
        raise AccountNotFoundError(account_id)
    return account


# ---------------- UPDATE ----------------
def update_account(account_id, name=None, number=None, balance=None):
    """Update account details."""
    account = Account.query.get(account_id)
    if not account:
        raise AccountNotFoundError(account_id)

    try:
        if name:
            account.name = name
        if number:
            account.number = number
        if balance is not None:
            account.balance = balance

        db.session.commit()

        message = f"""
✏️ Account Updated
-------------------------
Account ID: {account_id}
Updated Balance: {account.balance}
"""
        send_mail(account.email, "Account Updated Successfully", message, None)
        logger.info(message.strip())
        return account

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error updating account ID {account_id}: {e}")
        raise BMSException("Failed to update account.")


# ---------------- DELETE ----------------
def delete_account(account_id):
    """Delete an account."""
    account = Account.query.get(account_id)
    if not account:
        raise AccountNotFoundError(account_id)

    try:
        db.session.delete(account)
        db.session.commit()

        message = f"""
❌ Account Deleted
-------------------------
Account Number: {account.number}
"""
        send_mail(account.email, "Account Deleted", message, None)
        logger.info(message.strip())
        return True

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error deleting account ID {account_id}: {e}")
        raise BMSException("Failed to delete account.")


# ---------------- DEPOSIT ---------------
def deposit_money(account_number, amount):
    """Deposit money into an account."""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        raise AccountNotFoundError(account_number)

    try:
        account.balance += float(amount)
        db.session.commit()

        message = f"""
💰 Deposit Successful
-------------------------
Account Number: {account_number}
Amount Deposited: {amount}
New Balance: {account.balance}
"""
        send_mail(account.email, "Deposit Successful", message, None)
        logger.info(message.strip())
        return account, None

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error depositing money to {account_number}: {e}")
        raise BMSException("Deposit failed.")


# ---------------- WITHDRAW --------------
def withdraw_money(account_number, amount):
    """Withdraw money from an account."""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        raise AccountNotFoundError(account_number)

    if account.balance < float(amount):
        raise InsufficientFundsError(account_number)

    try:
        account.balance -= float(amount)
        db.session.commit()

        message = f"""
💸 Withdrawal Successful
-------------------------
Account Number: {account_number}
Amount Withdrawn: {amount}
Remaining Balance: {account.balance}
"""
        send_mail(account.email, "Withdrawal Successful", message, None)
        logger.info(message.strip())
        return account, None

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error withdrawing from {account_number}: {e}")
        raise BMSException("Withdrawal failed.")


# ---------------- TRANSFER --------------
def transfer_money(sender_number, receiver_number, amount):
    """Transfer money between two accounts."""
    sender = Account.query.filter_by(number=sender_number).first()
    receiver = Account.query.filter_by(number=receiver_number).first()

    if not sender or not receiver:
        raise InvalidTransferError()

    if sender.balance < float(amount):
        raise InsufficientFundsError(sender_number)

    try:
        sender.balance -= float(amount)
        receiver.balance += float(amount)
        db.session.commit()

        # Email both users
        send_mail(sender.email, "Money Sent",
                  f"Hi {sender.name}, you have sent ₹{amount} to {receiver.name}. New balance: ₹{sender.balance}.", None)

        send_mail(receiver.email, "Money Received",
                  f"Hi {receiver.name}, you received ₹{amount} from {sender.name}. Your new balance: ₹{receiver.balance}.", None)

        logger.info(f"Transfer successful: {amount} from {sender_number} to {receiver_number}")
        return (sender, receiver), None

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Error transferring money from {sender_number} to {receiver_number}: {e}")
        raise BMSException("Transfer failed.")


# ---------------- BATCH CALC --------------
def batch_calc():
    """Calculate total accounts, total balance, and average balance, then email summary to admin."""
    try:
        accounts = Account.query.all()
        total_accounts = len(accounts)
        total_balance = sum(acc.balance for acc in accounts)
        avg_balance = total_balance / total_accounts if total_accounts > 0 else 0

        # Prepare summary message
        message = f"""
🏦 Bank Balance Summary
----------------------------
Total Accounts: {total_accounts}
Total Balance: ₹{total_balance:.2f}
Average Balance: ₹{avg_balance:.2f}
"""
        # Send email to admin
        send_mail("abhishekojha786786@gmail.com", "Bank Balance Summary", message, None)
        logger.info("Batch calculation completed and summary email sent.")

        return {
            "total_accounts": total_accounts,
            "total_balance": total_balance,
            "average_balance": avg_balance
        }

    except Exception as e:
        logger.exception(f"Error during batch calculation: {e}")
        raise BMSException("Failed to calculate total balances.")

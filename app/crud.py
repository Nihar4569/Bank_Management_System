from app.models import Account
from app.db import db
from app.logger import logger
from app.email_utils import send_mail   # ✅ Email sender

# ---------------- CREATE ----------------
def create_account(name, number, balance, email):
    """Create a new account and send confirmation email."""
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


# ---------------- READ -----------------
def get_all_accounts():
    """Return all accounts."""
    return Account.query.all()

def get_account_by_id(account_id):
    """Return a single account by ID."""
    return Account.query.get(account_id)


# ---------------- UPDATE ----------------
def update_account(account_id, name=None, number=None, balance=None):
    """Update account details."""
    account = Account.query.get(account_id)
    if not account:
        logger.warning(f"Update failed - Account not found: ID {account_id}")
        return None

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


# ---------------- DELETE ----------------
def delete_account(account_id):
    """Delete an account."""
    account = Account.query.get(account_id)
    if not account:
        logger.warning(f"Delete failed - Account not found: ID {account_id}")
        return False

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


# ---------------- DEPOSIT ---------------
def deposit_money(account_number, amount):
    """Deposit money into an account."""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        logger.warning(f"Deposit failed - Account not found: {account_number}")
        return None, "Account not found"

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


# ---------------- WITHDRAW --------------
def withdraw_money(account_number, amount):
    """Withdraw money from an account."""
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        logger.warning(f"Withdraw failed - Account not found: {account_number}")
        return None, "Account not found"

    if account.balance < float(amount):
        logger.warning(f"Withdraw failed - Insufficient balance for {account_number}")
        return None, "Insufficient balance"

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


# ---------------- TRANSFER --------------
def transfer_money(sender_number, receiver_number, amount):
    """Transfer money between two accounts."""
    sender = Account.query.filter_by(number=sender_number).first()
    receiver = Account.query.filter_by(number=receiver_number).first()

    if not sender or not receiver:
        logger.warning(f"Transfer failed - Invalid accounts ({sender_number} → {receiver_number})")
        return None, "Invalid account number(s)"

    if sender.balance < float(amount):
        logger.warning(f"Transfer failed - Insufficient balance for {sender_number}")
        return None, "Insufficient balance"

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


# ---------------- BATCH CALC --------------
def batch_calc():
    """Calculate total accounts, total balance, and average balance, then email summary to admin."""
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

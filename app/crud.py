from app.models import Account
from app.db import db
from app.logger import logger

def create_account(name, number, balance):
    account = Account(name=name, number=number, balance=balance)
    db.session.add(account)
    db.session.commit()

    logger.info(f"Account created: {number} | Name: {name} | Balance: {balance}")
    return account


def get_all_accounts():
    return Account.query.all()


def get_account_by_id(account_id):
    return Account.query.get(account_id)

def update_account(account_id, name=None, number=None, balance=None):
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
    logger.info(f"Account updated: ID {account_id} | New Balance: {account.balance}")
    return account

def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        logger.warning(f"Delete failed - Account not found: ID {account_id}")
        return False

    db.session.delete(account)
    db.session.commit()
    logger.info(f"Account deleted: {account.number}")
    return True

def deposit_money(account_number, amount):
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        logger.warning(f"Deposit failed - Account not found: {account_number}")
        return None, "Account not found"

    account.balance += float(amount)
    db.session.commit()

    logger.info(f"Deposit successful: {amount} to {account_number} | New Balance: {account.balance}")
    return account, None

def withdraw_money(account_number, amount):
    account = Account.query.filter_by(number=account_number).first()
    if not account:
        logger.warning(f"Withdraw failed - Account not found: {account_number}")
        return None, "Account not found"

    if account.balance < float(amount):
        logger.warning(f"Withdraw failed - Insufficient balance for {account_number}")
        return None, "Insufficient balance"

    account.balance -= float(amount)
    db.session.commit()

    logger.info(f"Withdraw successful: {amount} from {account_number} | New Balance: {account.balance}")
    return account, None

def transfer_money(sender_number, receiver_number, amount):
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

    logger.info(f"Transfer successful: {amount} from {sender_number} to {receiver_number}")
    return (sender, receiver), None

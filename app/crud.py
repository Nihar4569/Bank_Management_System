from app.models import Account
from app.db import db

# CREATE
def create_account(name, number, balance):
    account = Account(name=name, number=number, balance=balance)
    db.session.add(account)
    db.session.commit()
    return account


# READ (all)
def get_all_accounts():
    return Account.query.all()


# READ (by ID)
def get_account_by_id(account_id):
    return Account.query.get(account_id)


# UPDATE
def update_account(account_id, name=None, number=None, balance=None):
    account = Account.query.get(account_id)
    if not account:
        return None

    if name:
        account.name = name
    if number:
        account.number = number
    if balance is not None:
        account.balance = balance

    db.session.commit()
    return account


# DELETE
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return False

    db.session.delete(account)
    db.session.commit()
    return True

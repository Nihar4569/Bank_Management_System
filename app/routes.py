from flask import Blueprint, jsonify, request

from app.crud import (
    create_account,
    get_all_accounts,
    get_account_by_id,
    update_account,
    delete_account,
    deposit_money,
    withdraw_money,
    transfer_money,
    batch_calc
)
from app.batch_calc import calc_total_balance

# Create a Blueprint (like a mini app inside Flask)
bp = Blueprint('routes', __name__)

# CREATE - POST /accounts
@bp.route('/accounts', methods=['POST'])
def add_account():
    data = request.get_json()
    name = data.get('name')
    number = data.get('number')
    balance = data.get('balance')
    email = data.get('email')

    if not all([name, number, email]):
        return jsonify({"error": "Missing required fields"}), 400


    account = create_account(name, number, balance, email)
    return jsonify({
        "id": account.id,
        "name": account.name,
        "number": account.number,
        "balance": account.balance,
        "email": account.email
    }), 201


# READ - GET /accounts
@bp.route('/accounts', methods=['GET'])
def list_accounts():
    accounts = get_all_accounts()
    result = [
        {"id": a.id, "name": a.name, "number": a.number, "balance": a.balance}
        for a in accounts
    ]
    return jsonify(result), 200


# READ - GET /accounts/<id>
@bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = get_account_by_id(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "id": account.id,
        "name": account.name,
        "number": account.number,
        "balance": account.balance
    })


# UPDATE - PUT /accounts/<id>
@bp.route('/accounts/<int:account_id>', methods=['PUT'])
def edit_account(account_id):
    data = request.get_json()
    account = update_account(
        account_id,
        name=data.get('name'),
        number=data.get('number'),
        balance=data.get('balance')
    )
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": "Account updated successfully"})


# DELETE - DELETE /accounts/<id>
@bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def remove_account(account_id):
    success = delete_account(account_id)
    if not success:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": "Account deleted successfully"})

# DEPOSIT - POST /accounts/deposit
@bp.route('/accounts/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    acc_number = data.get('number')
    amount = data.get('amount')

    if not acc_number or amount is None:
        return jsonify({"error": "Account number and amount required"}), 400

    account, error = deposit_money(acc_number, amount)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": f"Deposited {amount} successfully",
        "balance": account.balance
    }), 200


# WITHDRAW - POST /accounts/withdraw
@bp.route('/accounts/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    acc_number = data.get('number')
    amount = data.get('amount')

    if not acc_number or amount is None:
        return jsonify({"error": "Account number and amount required"}), 400

    account, error = withdraw_money(acc_number, amount)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": f"Withdrawn {amount} successfully",
        "balance": account.balance
    }), 200


# TRANSFER - POST /accounts/transfer
@bp.route('/accounts/transfer', methods=['POST'])
def transfer():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')

    if not all([sender, receiver, amount is not None]):
        return jsonify({"error": "Sender, receiver, and amount required"}), 400

    result, error = transfer_money(sender, receiver, amount)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": f"Transferred {amount} from {sender} to {receiver} successfully"
    }), 200
    
# 🏦 BATCH CALCULATION ENDPOINT
@bp.route("/batch_calc", methods=["GET"])
def calculate_total_balance():
    result = batch_calc()
    return jsonify(result), 200
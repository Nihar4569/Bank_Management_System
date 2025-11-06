from flask import Blueprint, request, jsonify
from app.crud import (
    create_account,
    get_all_accounts,
    get_account_by_id,
    update_account,
    delete_account
)

# Create a Blueprint (like a mini app inside Flask)
bp = Blueprint('routes', __name__)

# CREATE - POST /accounts
@bp.route('/accounts', methods=['POST'])
def add_account():
    data = request.get_json()
    name = data.get('name')
    number = data.get('number')
    balance = data.get('balance')

    if not all([name, number, balance is not None]):
        return jsonify({"error": "Missing fields"}), 400

    account = create_account(name, number, balance)
    return jsonify({
        "id": account.id,
        "name": account.name,
        "number": account.number,
        "balance": account.balance
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

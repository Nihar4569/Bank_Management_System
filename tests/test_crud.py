# tests/test_crud.py
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_create_account():
    data = {
        "name": "Test User",
        "number": "5550001111",
        "email": "testuser@gmail.com",
        "balance": 1000
    }
    response = requests.post(f"{BASE_URL}/accounts", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "Test User"
    assert "id" in result

def test_get_accounts():
    response = requests.get(f"{BASE_URL}/accounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_deposit_money():
    data = {"number": "5550001111", "amount": 500}
    response = requests.post(f"{BASE_URL}/accounts/deposit", json=data)
    assert response.status_code == 200
    assert "balance" in response.json()

def test_withdraw_money():
    data = {"number": "5550001111", "amount": 200}
    response = requests.post(f"{BASE_URL}/accounts/withdraw", json=data)
    assert response.status_code == 200
    assert "balance" in response.json()

def test_update_account():
    # get first account id
    acc_list = requests.get(f"{BASE_URL}/accounts").json()
    acc_id = acc_list[0]["id"]
    data = {"name": "Updated User"}
    response = requests.put(f"{BASE_URL}/accounts/{acc_id}", json=data)
    assert response.status_code == 200

def test_delete_account():
    # create a temporary account first
    data = {
        "name": "Delete User",
        "number": "8889990001",
        "email": "deleteuser@gmail.com",
        "balance": 500
    }
    new_acc = requests.post(f"{BASE_URL}/accounts", json=data).json()
    acc_id = new_acc["id"]

    response = requests.delete(f"{BASE_URL}/accounts/{acc_id}")
    assert response.status_code == 200

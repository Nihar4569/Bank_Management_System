import requests

BASE_URL = "http://127.0.0.1:5000"

def test_deposit():
    """Deposit into existing account."""
    payload = {"number": "10001", "amount": 1000}
    res = requests.post(f"{BASE_URL}/accounts/deposit", json=payload)
    assert res.status_code == 200
    assert "balance" in res.json()


def test_withdraw():
    """Withdraw from existing account."""
    payload = {"number": "10001", "amount": 500}
    res = requests.post(f"{BASE_URL}/accounts/withdraw", json=payload)
    assert res.status_code == 200
    assert "balance" in res.json()


def test_transfer():
    """Transfer money between accounts."""
    payload = {"sender": "10002", "receiver": "10003", "amount": 250}
    res = requests.post(f"{BASE_URL}/accounts/transfer", json=payload)
    assert res.status_code == 200
    assert "Transferred" in res.json()["message"]

# tests/test_exceptions.py
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_account_not_found():
    """Should return 404 for non-existing account."""
    res = requests.get(f"{BASE_URL}/accounts/99999")
    assert res.status_code in (400, 404)
    j = res.json()
    assert "error" in j


def test_invalid_deposit():
    """Deposit should fail if missing fields."""
    res = requests.post(f"{BASE_URL}/accounts/deposit", json={})
    assert res.status_code == 400
    j = res.json()
    assert "error" in j


def test_invalid_transfer():
    """Invalid transfer request should fail."""
    data = {"sender": "999", "receiver": "888", "amount": 100}
    res = requests.post(f"{BASE_URL}/accounts/transfer", json=data)
    assert res.status_code in (400, 404)
    j = res.json()
    assert "error" in j

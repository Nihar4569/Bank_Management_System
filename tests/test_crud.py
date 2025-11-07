import requests

BASE_URL = "http://127.0.0.1:5000"

def test_create_accounts():
    """Create new accounts."""
    users = [
        {"name": "Nihar", "number": "10001", "email": "nihar4569@gmail.com", "balance": 2000},
        {"name": "Rishabh", "number": "10002", "email": "iamrishabh1000@gmail.com", "balance": 2500},
        {"name": "Sahu", "number": "10003", "email": "sahun4569@gmail.com", "balance": 3000},
        {"name": "Rishabh Singh", "number": "10004", "email": "rishabhsingh29yes@gmail.com", "balance": 4000},
    ]

    for user in users:
        res = requests.post(f"{BASE_URL}/accounts", json=user)
        assert res.status_code in (200, 201)
        data = res.json()
        assert "id" in data
        assert data["name"] == user["name"]


def test_get_accounts():
    """Check if accounts list is returned."""
    res = requests.get(f"{BASE_URL}/accounts")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 4

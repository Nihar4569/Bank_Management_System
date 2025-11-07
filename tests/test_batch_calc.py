import requests

BASE_URL = "http://127.0.0.1:5000"

def test_batch_calc():
    """Ensure total balance and accounts are correctly computed."""

    # Create test accounts before calling batch_calc
    sample_accounts = [
        {"name": "Nihar", "number": "1111", "email": "nihar4569@gmail.com", "balance": 1000},
        {"name": "Rishabh", "number": "2222", "email": "iamrishabh1000@gmail.com", "balance": 2000},
        {"name": "Sahu", "number": "3333", "email": "sahun4569@gmail.com", "balance": 3000},
        # {"name": "Maheshwar", "number": "9750592159", "email": "gmaheswaranmca@gmail.com", "balance": 3000}
    ]
    for acc in sample_accounts:
        requests.post(f"{BASE_URL}/accounts", json=acc)

    # Test batch calculation
    res = requests.get(f"{BASE_URL}/batch_calc")
    assert res.status_code == 200

    data = res.json()
    assert "total_accounts" in data
    assert "total_balance" in data
    assert "average_balance" in data

    # Should now be > 0
    assert data["total_accounts"] > 0
    assert data["total_balance"] > 0
    assert data["average_balance"] > 0

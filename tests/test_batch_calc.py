# tests/test_batch_calc.py
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_batch_calc():
    response = requests.get(f"{BASE_URL}/batch_calc")
    assert response.status_code == 200
    data = response.json()

    assert "total_accounts" in data
    assert "total_balance" in data
    assert "average_balance" in data
    assert isinstance(data["total_accounts"], int)
    assert isinstance(data["total_balance"], (int, float))

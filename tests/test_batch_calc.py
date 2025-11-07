# tests/test_batch_calc.py
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_batch_calc():
    """Test total balance calculation endpoint."""
    res = requests.get(f"{BASE_URL}/batch_calc")
    assert res.status_code == 200
    data = res.json()
    assert "total_accounts" in data
    assert "total_balance" in data
    assert "average_balance" in data
    assert data["total_accounts"] > 0

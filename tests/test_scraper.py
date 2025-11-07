import requests

BASE_URL = "http://127.0.0.1:5000"

def test_interest_rates():
    res = requests.get(f"{BASE_URL}/scrape/interest-rates")
    assert res.status_code == 200
    data = res.json()
    print("Interest Rates Data:", data[:2])
    assert isinstance(data, list)
    assert len(data) > 0

def test_bank_names():
    res = requests.get(f"{BASE_URL}/scrape/bank-names")
    assert res.status_code == 200
    data = res.json()["banks"]
    print("Banks:", data)
    assert isinstance(data, list)
    assert len(data) > 0

test_interest_rates()
test_bank_names()

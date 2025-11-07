# tests/test_scraper.py
from app.scraper import scrape_interest_rates, scrape_bank_names

def test_scrape_interest_rates():
    """Ensure scraper returns structured bank data."""
    data = scrape_interest_rates()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("bank" in d for d in data)
    assert all("info" in d for d in data)


def test_scrape_bank_names():
    """Ensure scraper fetches some bank names."""
    data = scrape_bank_names()
    assert isinstance(data, list)
    assert all(isinstance(name, str) for name in data)

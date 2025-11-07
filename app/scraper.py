import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.logger import logger

# Example sites with interest rates (can change if unavailable)
BANK_URLS = {
    "SBI": "https://www.sbi.co.in/web/interest-rates/deposit-rates",
    "HDFC": "https://www.hdfcbank.com/personal/resources/rates",
    "ICICI": "https://www.icicibank.com/Personal-Banking/deposits/fixed-deposit-interest-rates.page",
}


def fetch_interest_rate(bank_name, url):
    """Fetch interest rate data for a single bank."""
    try:
        logger.info(f"Fetching rates for {bank_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Simplified parsing (depends on page layout)
        text = soup.get_text().lower()
        keywords = ["interest", "rate", "%", "deposit"]

        # Extract a few lines containing keywords
        lines = [line.strip() for line in text.split("\n") if any(k in line for k in keywords)]
        snippet = "\n".join(lines[:10])  # take first 10 lines as summary

        logger.info(f"Successfully scraped data for {bank_name}")
        return {"bank": bank_name, "url": url, "info": snippet}

    except Exception as e:
        logger.warning(f"Failed to fetch {bank_name}: {e}")
        return {"bank": bank_name, "url": url, "info": "Error fetching data"}


def scrape_interest_rates():
    """Scrape interest rate info for all banks concurrently."""
    logger.info("Starting concurrent scraping for interest rates...")

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_bank = {executor.submit(fetch_interest_rate, bank, url): bank for bank, url in BANK_URLS.items()}
        for future in as_completed(future_to_bank):
            bank = future_to_bank[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Error scraping {bank}: {e}")

    logger.info("Scraping completed for all banks.")
    return results


def scrape_bank_names():
    """Scrape bank names from RBI official list."""
    try:
        url = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        banks = [a.text.strip() for a in soup.find_all("a") if "Bank" in a.text]
        unique_banks = list(set(banks))[:15]

        logger.info(f"✅ Scraped {len(unique_banks)} bank names from RBI site.")
        return unique_banks
    except Exception as e:
        logger.warning(f"Failed to fetch RBI bank list: {e}")
        return []

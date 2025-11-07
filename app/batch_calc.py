from concurrent.futures import ThreadPoolExecutor
from app.models import Account
from app.db import get_db_session

def calc_total_balance():
    """Calculate total balance using index-based batch division."""
    session = get_db_session()
    accounts = session.query(Account).all()
    session.close()

    balances = [acc.balance for acc in accounts]
    n = len(balances)
    batch_size = 10  

    # Function to process a range of indices
    def process_range(start_idx, end_idx):
        total = 0
        for i in range(start_idx, end_idx):
            if i < n:
                total += balances[i]
        print(f"Processed accounts[{start_idx}:{end_idx}] = {total}")
        return total

    total_sum = 0
    index_ranges = [(i, i + batch_size) for i in range(0, n, batch_size)]  #[(0, 10), (10, 20), (20, 30), ...]

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_range, start, end) for start, end in index_ranges]

        for future in futures:
            total_sum += future.result()

    return total_sum

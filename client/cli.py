#!/usr/bin/env python3
"""
==================================================================
🏦 Banking Management System (BMS) — CLI Client
==================================================================

A professional-grade command-line interface for interacting with
the Flask-based BMS REST API.

Features:
- CRUD Operations on Accounts
- Batch Balance Calculation
- Web Scraping (Interest Rates)
- Structured Logging
- Colorized Console Output

Author: Your Name
Version: 1.0.0
==================================================================
"""

import sys
import argparse
import logging
import requests
from rich.console import Console
from rich.table import Table
from rich import box

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
BASE_URL = "http://127.0.0.1:5000"
LOG_FILE = "client.log"

# Rich console for colorful output
console = Console()

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
def handle_response(response):
    """Validate and print API responses."""
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        console.print(f"[bold red]HTTP Error:[/bold red] {http_err}")
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Connection Error:[/bold red] Unable to reach API.")
    except requests.exceptions.Timeout:
        console.print("[bold red]Timeout:[/bold red] The request timed out.")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
    return None


# -------------------------------------------------------------
# CLI Command Implementations
# -------------------------------------------------------------
def list_accounts():
    """List all accounts."""
    res = requests.get(f"{BASE_URL}/accounts")
    data = handle_response(res)
    if not data:
        console.print("[yellow]No accounts found.[/yellow]")
        return

    table = Table(title="Bank Accounts", box=box.ROUNDED, style="cyan")
    table.add_column("ID", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Number", style="magenta")
    table.add_column("Balance", justify="right", style="bold yellow")

    for acc in data:
        table.add_row(str(acc["id"]), acc["name"], acc["number"], f"{acc['balance']:.2f}")

    console.print(table)
    logger.info("Listed all accounts.")


def get_account(acc_id):
    """Retrieve account details by ID."""
    res = requests.get(f"{BASE_URL}/accounts/{acc_id}")
    data = handle_response(res)
    if not data:
        console.print(f"[red]Account with ID {acc_id} not found.[/red]")
        return

    console.print(f"\n[bold cyan]Account Details (ID: {acc_id})[/bold cyan]")
    console.print(f"👤 Name: {data['name']}")
    console.print(f"🏦 Number: {data['number']}")
    console.print(f"💰 Balance: ₹{data['balance']:.2f}")
    logger.info(f"Fetched account {acc_id}.")


def create_account(name, number, balance):
    """Create a new account."""
    payload = {"name": name, "number": number, "balance": float(balance)}
    res = requests.post(f"{BASE_URL}/accounts", json=payload)
    data = handle_response(res)
    if data:
        console.print("[green]✅ Account created successfully![/green]")
        logger.info(f"Created account: {data}")
    else:
        logger.error("Failed to create account.")


def update_account(acc_id, name=None, number=None, balance=None):
    """Update existing account details."""
    payload = {}
    if name:
        payload["name"] = name
    if number:
        payload["number"] = number
    if balance is not None:
        payload["balance"] = float(balance)

    res = requests.put(f"{BASE_URL}/accounts/{acc_id}", json=payload)
    data = handle_response(res)
    if data:
        console.print("[cyan]✏️ Account updated successfully![/cyan]")
        logger.info(f"Updated account {acc_id}")
    else:
        logger.error(f"Failed to update account {acc_id}.")


def delete_account(acc_id):
    """Delete an account by ID."""
    res = requests.delete(f"{BASE_URL}/accounts/{acc_id}")
    if res.status_code == 404:
        console.print(f"[red]Account with ID {acc_id} not found.[/red]")
        return
    console.print("[bold red]🗑️ Account deleted successfully![/bold red]")
    logger.info(f"Deleted account {acc_id}.")


def total_balance():
    """Run batch total balance computation."""
    res = requests.get(f"{BASE_URL}/batch/total")
    data = handle_response(res)
    if data:
        total = data.get("total_balance", 0)
        console.print(f"[bold green]💰 Total Balance across all accounts: ₹{total:.2f}[/bold green]")
        logger.info("Fetched total balance.")


def interest_rates():
    """Fetch interest rates via web scraper."""
    res = requests.get(f"{BASE_URL}/scraper/rates")
    data = handle_response(res)
    if not data:
        console.print("[red]No interest rate data available.[/red]")
        return

    table = Table(title="🏦 Current Interest Rates", box=box.SIMPLE, style="magenta")
    table.add_column("Bank", style="cyan")
    table.add_column("Rate (%)", justify="right", style="yellow")

    for bank, rate in data.items():
        table.add_row(bank, str(rate))

    console.print(table)
    logger.info("Fetched interest rates.")


# -------------------------------------------------------------
# CLI Argument Parser
# -------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="CLI Client for the Banking Management System (BMS)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # CRUD commands
    subparsers.add_parser("list", help="List all accounts")

    get_p = subparsers.add_parser("get", help="Get an account by ID")
    get_p.add_argument("id", type=int, help="Account ID")

    create_p = subparsers.add_parser("create", help="Create a new account")
    create_p.add_argument("name", help="Account holder name")
    create_p.add_argument("number", help="Account number")
    create_p.add_argument("balance", type=float, help="Initial balance")

    update_p = subparsers.add_parser("update", help="Update an existing account")
    update_p.add_argument("id", type=int, help="Account ID")
    update_p.add_argument("--name", help="Updated name")
    update_p.add_argument("--number", help="Updated number")
    update_p.add_argument("--balance", type=float, help="Updated balance")

    delete_p = subparsers.add_parser("delete", help="Delete an account")
    delete_p.add_argument("id", type=int, help="Account ID")

    # Other commands
    subparsers.add_parser("total", help="Run batch total balance calculation")
    subparsers.add_parser("rates", help="Fetch web-scraped interest rates")

    args = parser.parse_args()

    # Command routing
    commands = {
        "list": list_accounts,
        "get": lambda: get_account(args.id),
        "create": lambda: create_account(args.name, args.number, args.balance),
        "update": lambda: update_account(args.id, args.name, args.number, args.balance),
        "delete": lambda: delete_account(args.id),
        "total": total_balance,
        "rates": interest_rates,
    }

    try:
        commands[args.command]()
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user.[/red]")
        logger.warning("Operation cancelled by user.")
        sys.exit(1)


# -------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------
if __name__ == "__main__":
    main()

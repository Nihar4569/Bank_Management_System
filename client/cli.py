import requests

BASE_URL = "http://127.0.0.1:5000"

def create_account():
    name = input("Enter account holder name: ")
    number = input("Enter account number: ")
    email = input("Enter email address: ")
    balance = float(input("Enter opening balance: "))

    data = {
        "name": name,
        "number": number,
        "email": email,
        "balance": balance
    }

    response = requests.post(f"{BASE_URL}/accounts", json=data)
    print_response(response)


def list_accounts():
    response = requests.get(f"{BASE_URL}/accounts")
    print_response(response)


def deposit():
    number = input("Enter account number: ")
    amount = float(input("Enter amount to deposit: "))

    data = {"number": number, "amount": amount}
    response = requests.post(f"{BASE_URL}/accounts/deposit", json=data)
    print_response(response)


def withdraw():
    number = input("Enter account number: ")
    amount = float(input("Enter amount to withdraw: "))

    data = {"number": number, "amount": amount}
    response = requests.post(f"{BASE_URL}/accounts/withdraw", json=data)
    print_response(response)


def transfer():
    sender = input("Enter sender account number: ")
    receiver = input("Enter receiver account number: ")
    amount = float(input("Enter amount to transfer: "))

    data = {
        "sender_number": sender,
        "receiver_number": receiver,
        "amount": amount
    }
    response = requests.post(f"{BASE_URL}/accounts/transfer", json=data)
    print_response(response)


def batch_calc():
    response = requests.get(f"{BASE_URL}/batch_calc")
    print_response(response)


def print_response(response):
    print("\nStatus Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)
    print("\n-----------------------------------\n")


def main():
    print("\n===== BANK MANAGEMENT SYSTEM CLIENT =====")
    print("1. Create Account")
    print("2. List All Accounts")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Batch Total Balance")
    print("7. Exit")

    while True:
        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            list_accounts()
        elif choice == "3":
            deposit()
        elif choice == "4":
            withdraw()
        elif choice == "5":
            transfer()
        elif choice == "6":
            batch_calc()
        elif choice == "7":
            print("Exiting client. Goodbye!")
            break
        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()

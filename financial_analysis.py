import os
import pandas as pd


def load_transaction_data():
    path = "data/banking_transactions.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    data = pd.read_csv(path)
    if "amount" not in data.columns:
        raise ValueError("The transaction data file must include an 'amount' column.")

    return data


def analyze_financial_data():
    data = load_transaction_data()

    total_transactions = len(data)
    total_amount = data['amount'].sum()
    average_transaction = data['amount'].mean()
    highest_transaction = data['amount'].max()
    lowest_transaction = data['amount'].min()

    analysis = {
        "Total Transactions": total_transactions,
        "Total Amount": round(total_amount, 2),
        "Average Transaction": round(average_transaction, 2),
        "Highest Transaction": highest_transaction,
        "Lowest Transaction": lowest_transaction
    }

    return analysis

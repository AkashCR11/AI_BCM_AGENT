import os
import pandas as pd
from sklearn.ensemble import IsolationForest


def load_transaction_data():
    path = "data/banking_transactions.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    data = pd.read_csv(path)
    if "amount" not in data.columns:
        raise ValueError("The transaction data file must include an 'amount' column.")

    return data


def detect_fraud():
    data = load_transaction_data()

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    data['Fraud_Prediction'] = model.fit_predict(
        data[['amount']]
    )

    fraud_cases = data[
        data['Fraud_Prediction'] == -1
    ]

    return fraud_cases
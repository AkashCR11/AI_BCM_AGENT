import os
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest


def load_transaction_data():
    path = "data/banking_transactions.csv"

    # ✅ Debug info (very important)
    st.write("📂 Current directory:", os.getcwd())
    st.write("📁 Files in root:", os.listdir())

    if os.path.exists("data"):
        st.write("📁 Files inside data folder:", os.listdir("data"))
    else:
        st.write("❌ 'data' folder NOT found")

    st.write("✅ File exists:", os.path.exists(path))

    # ✅ Try loading file
    try:
        data = pd.read_csv(path)

        if "amount" not in data.columns:
            raise ValueError("CSV must contain 'amount' column")

        return data

    except Exception as e:
        # ✅ Fallback (so app doesn't break)
        st.error("⚠️ Using fallback sample data")

        return pd.DataFrame({
            "transaction_id": [1, 2, 3, 4],
            "amount": [1000, 5000, 200, 10000]
        })


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

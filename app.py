import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from chatbot import ask_ai
from test_case_generator import generate_test_cases
from fraud_detection import detect_fraud
from financial_analysis import analyze_financial_data
from agent import agent_router

# PAGE CONFIG
st.set_page_config(
    page_title="AI BCM Agent",
    page_icon="🤖",
    layout="wide"
)

# TITLE
st.title("🤖 AI BCM & Capital Market Testing Assistant")

st.markdown("""
This AI Agent helps with:
- Banking Queries  
- AI Test Case Generation  
- Fraud Detection  
- Financial Analysis  
- Capital Market Insights  
""")

# SIDEBAR MENU
menu = st.sidebar.selectbox(
    "Select Module",
    [
        "AI Banking Chatbot",
        "AI Test Case Generator",
        "Fraud Detection",
        "Financial Analysis"
    ]
)

# -------------------------------------------
# AI CHATBOT
# -------------------------------------------
if menu == "AI Banking Chatbot":
    st.header("💬 AI Banking Chatbot")

    question = st.text_area(
        "Ask Banking or Capital Market Questions"
    )

    if st.button("Generate AI Response"):
        try:
            with st.spinner("Generating Response..."):
                answer = agent_router(question)
                st.success("AI Response Generated")
                st.write(answer)
        except Exception as error:
            st.error("Unable to generate AI response.")
            st.exception(error)

# -------------------------------------------
# TEST CASE GENERATOR
# -------------------------------------------
elif menu == "AI Test Case Generator":
    st.header("🧪 AI Test Case Generator")

    module_name = st.text_input(
        "Enter Banking Module Name"
    )

    if st.button("Generate Test Cases"):
        if not module_name or not module_name.strip():
            st.warning("Please enter a module name before generating test cases.")
        else:
            try:
                with st.spinner("Generating Test Cases..."):
                    test_cases = generate_test_cases(module_name)
                    st.success("Test Cases Generated")
                    st.write(test_cases)
            except Exception as error:
                st.error("Unable to generate test cases.")
                st.exception(error)

# -------------------------------------------
# FRAUD DETECTION
# -------------------------------------------
elif menu == "Fraud Detection":
    st.header("🚨 AI Fraud Detection")

    if st.button("Run Fraud Detection"):
        try:
            fraud_data = detect_fraud()
            st.subheader("Suspicious Transactions")
            st.dataframe(fraud_data)
        except Exception as error:
            st.error("Unable to run fraud detection.")
            st.exception(error)

# -------------------------------------------
# FINANCIAL ANALYSIS
# -------------------------------------------
elif menu == "Financial Analysis":
    st.header("📊 Financial Analysis Dashboard")

    try:
        analysis = analyze_financial_data()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Transactions", analysis['Total Transactions'])
            st.metric("Total Amount", analysis['Total Amount'])

        with col2:
            st.metric("Average Transaction", analysis['Average Transaction'])
            st.metric("Highest Transaction", analysis['Highest Transaction'])

        data = pd.read_csv("data/banking_transactions.csv")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['transaction_id'], data['amount'])
        ax.set_title("Transaction Amount Analysis")
        ax.set_xlabel("Transaction ID")
        ax.set_ylabel("Amount")
        st.pyplot(fig)
    except Exception as error:
        st.error("Unable to load financial analysis data.")
        st.exception(error)

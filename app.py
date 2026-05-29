import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from agent import agent_router
from test_case_generator import generate_test_cases
from fraud_detection import detect_fraud
from financial_analysis import analyze_financial_data


# -------------------------------------------
# PAGE CONFIG
# -------------------------------------------
st.set_page_config(
    page_title="AI BCM Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI - Banking & Capital Market Assistant")
st.caption("Powered by Azure GPT-4o + Agentic AI")

# -------------------------------------------
# MEMORY (ChatGPT style)
# -------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------------------
# SIDEBAR
# -------------------------------------------
with st.sidebar:
    st.header("📌 Select Module")
    menu = st.selectbox(
        "",
        [
            "AI Banking Chatbot",
            "AI Test Case Generator",
            "Fraud Detection",
            "Financial Analysis"
        ]
    )

    st.markdown("---")
    st.markdown("### ✅ Features")
    st.markdown("""
    - GPT‑4o Chatbot  
    - Agentic AI Routing  
    - Fraud Detection  
    - Test Case Generator  
    - Financial Analytics  
    - PDF RAG Support ✅
    """)

# -------------------------------------------
# AI CHATBOT (AGENTIC + MEMORY + RAG)
# -------------------------------------------
if menu == "AI Banking Chatbot":
    st.header("💬 AI Banking Agent")

    # ✅ PDF Upload (RAG)
    uploaded_file = st.file_uploader("📄 Upload PDF for AI Analysis", type="pdf")

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        st.success("✅ PDF uploaded successfully. You can now ask questions about it!")

    # Display history first
    for role, message in st.session_state.history:
        with st.chat_message(role):
            st.markdown(message)

    # Chat input
    user_input = st.chat_input("Ask banking or capital market questions...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message
        st.session_state.history.append(("user", user_input))

        try:
            with st.spinner("AI Agent thinking..."):
                response = agent_router(user_input)

            # Show assistant response
            with st.chat_message("assistant"):
                st.markdown(response)

            # Save response
            st.session_state.history.append(("assistant", response))

        except Exception as error:
            st.error("Unable to generate response.")
            st.exception(error)

# -------------------------------------------
# TEST CASE GENERATOR
# -------------------------------------------
elif menu == "AI Test Case Generator":
    st.header("🧪 AI Test Case Generator")

    module_name = st.text_input("Enter Banking Module Name")

    if st.button("Generate Test Cases"):
        if not module_name or not module_name.strip():
            st.warning("Please enter a module name.")
        else:
            try:
                with st.spinner("Generating Test Cases..."):
                    test_cases = generate_test_cases(module_name)

                st.success("Test Cases Generated ✅")
                st.markdown(test_cases)

            except Exception as error:
                st.error("Error generating test cases.")
                st.exception(error)

# -------------------------------------------
# FRAUD DETECTION
# -------------------------------------------
elif menu == "Fraud Detection":
    st.header("🚨 AI Fraud Detection")

    if st.button("Run Fraud Detection"):
        try:
            with st.spinner("Analyzing transactions..."):
                fraud_data = detect_fraud()

            st.subheader("Suspicious Transactions")
            st.dataframe(fraud_data)

        except Exception as error:
            st.error("Fraud detection failed.")
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

        # Load data
        data = pd.read_csv("data/banking_transactions.csv")

        # Plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['transaction_id'], data['amount'])
        ax.set_title("Transaction Amount Analysis")
        ax.set_xlabel("Transaction ID")
        ax.set_ylabel("Amount")

        st.pyplot(fig)

    except Exception as error:
        st.error("Financial analysis failed.")
        st.exception(error)

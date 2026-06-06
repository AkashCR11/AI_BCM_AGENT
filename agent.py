import os
import streamlit as st

from chatbot import ask_ai
from fraud_detection import detect_fraud
from rag import rag_pipeline
from repo_agent import repo_agent
from file_processor import process_excel


# ✅ -------------------------------
# MEMORY INITIALIZATION (SAFE)
# ✅ -------------------------------
if "memory" not in st.session_state:
    st.session_state["memory"] = []


def agent_router(user_query):
    query = user_query.lower()

    # ✅ SAFELY GET MEMORY
    if "memory" not in st.session_state:
        st.session_state["memory"] = []

    memory = st.session_state["memory"]

    # ✅ STORE USER QUERY
    memory.append({
        "role": "user",
        "content": user_query
    })

    # ✅ -------------------------------
    # STEP 1 — REPO KNOWLEDGE
    # ✅ -------------------------------
    repo_response = repo_agent(user_query)

    # ✅ -------------------------------
    # STEP 2 — MULTI-TOOL CHAINING
    # (Repo + Document)
    # ✅ -------------------------------
    if ("pdf" in query or "document" in query) and repo_response:

        file_path = st.session_state.get("file_path", "temp.pdf")

        if os.path.exists(file_path):
            try:
                rag_answer, _ = rag_pipeline(file_path, user_query)
            except Exception:
                rag_answer = "⚠️ Unable to process document."
        else:
            rag_answer = "⚠️ No document uploaded."

        response = (
            "🧠 Combined AI Response\n\n"
            "📦 Repo Knowledge:\n" + repo_response + "\n\n"
            "📄 Document Insight:\n" + rag_answer
        )

        memory.append({
            "role": "assistant",
            "content": response
        })

        return response

    # ✅ If repo alone is enough
    if repo_response:
        memory.append({
            "role": "assistant",
            "content": repo_response
        })
        return repo_response

    # ✅ -------------------------------
    # STEP 3 — RULE-BASED DECISION
    # ✅ -------------------------------
    if "fraud" in query:
        action = "fraud_detection"

    elif "test case" in query:
        action = "test_case_generation"

    elif "analysis" in query or "financial" in query:
        action = "financial_analysis"

    elif "pdf" in query or "document" in query:
        action = "rag"

    elif "excel" in query:
        try:
            file_path = st.session_state.get("file_path", None)

            if file_path and file_path.endswith(".xlsx"):
                excel_data = process_excel(file_path)

                response = "📊 Excel Data Preview:\n\n" + excel_data
            else:
                response = "⚠️ Please upload an Excel file."

        except Exception:
            response = "⚠️ Error processing Excel file."

        memory.append({
            "role": "assistant",
            "content": response
        })

        return response

    else:
        # ✅ -------------------------------
        # STEP 4 — LLM DECISION WITH MEMORY
        # ✅ -------------------------------
        decision_prompt = (
            "You are an intelligent AI agent.\n\n"
            "Available actions:\n"
            "- fraud_detection\n"
            "- test_case_generation\n"
            "- financial_analysis\n"
            "- rag\n"
            "- general_chat\n\n"
            f"Conversation history:\n{memory}\n\n"
            f"Query: {user_query}\n\n"
            "Return ONLY one action."
        )

        decision = ask_ai(decision_prompt).lower().strip()

        if "fraud" in decision:
            action = "fraud_detection"
        elif "test" in decision:
            action = "test_case_generation"
        elif "analysis" in decision:
            action = "financial_analysis"
        elif "rag" in decision:
            action = "rag"
        else:
            action = "general_chat"

    # ✅ -------------------------------
    # STEP 5 — EXECUTE ACTION
    # ✅ -------------------------------

    if action == "fraud_detection":
        fraud_data = detect_fraud()

        summary = ask_ai(
            "Analyze this fraud data:\n" + fraud_data.to_string()
        )

        response = (
            "🚨 Fraud Detection Results\n\n"
            + fraud_data.to_string()
            + "\n\n📊 Insights:\n"
            + summary
        )

    elif action == "test_case_generation":
        response = ask_ai(
            "Generate detailed test cases for: " + user_query
        )

    elif action == "financial_analysis":
        response = ask_ai(
            "Provide financial analysis for: " + user_query
        )

    elif action == "rag":
        file_path = st.session_state.get("file_path", "temp.pdf")

        if not os.path.exists(file_path):
            response = "⚠️ Please upload a document first."
        else:
            try:
                answer, _ = rag_pipeline(file_path, user_query)
                response = "📄 Document-Based Answer\n\n" + answer
            except Exception:
                response = "⚠️ Error processing document."

    else:
        response = ask_ai(user_query)

    # ✅ STORE ASSISTANT RESPONSE
    memory.append({
        "role": "assistant",
        "content": response
    })

    return response

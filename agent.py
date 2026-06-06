import os
import streamlit as st

from chatbot import ask_ai
from fraud_detection import detect_fraud
from rag import rag_pipeline
from repo_agent import repo_agent
from file_processor import process_excel
from database import get_product_modules


# ✅ -------------------------------
# MEMORY INIT
# ✅ -------------------------------
if "memory" not in st.session_state:
    st.session_state["memory"] = []


def agent_router(user_query):
    query = user_query.lower()

    # ✅ SAFE MEMORY ACCESS
    if "memory" not in st.session_state:
        st.session_state["memory"] = []

    memory = st.session_state["memory"]

    # ✅ STORE USER INPUT
    memory.append({"role": "user", "content": user_query})

    # ------------------------------------------
    # ✅ COMPARISON FEATURE
    # ------------------------------------------
    products_list = ["flexcube", "finnacle", "q2"]

    if "compare" in query:
        matched = [p for p in products_list if p in query]

        if len(matched) >= 2:
            p1, p2 = matched[:2]

            comparison_prompt = f"""
Compare the following banking products:

Product 1: {p1}
Product 2: {p2}

Compare based on:
- Features
- Use cases
- Strengths

Provide structured output.
"""
            response = ask_ai(comparison_prompt)

            memory.append({"role": "assistant", "content": response})
            return response

    # ------------------------------------------
    # ✅ REPO RESPONSE
    # ------------------------------------------
    repo_response = repo_agent(user_query)

    # ------------------------------------------
    # ✅ MULTI-TOOL: REPO + RAG
    # ------------------------------------------
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

        memory.append({"role": "assistant", "content": response})
        return response

    # ------------------------------------------
    # ✅ REPO + LLM EXPLANATION + RECOMMENDATION
    # ------------------------------------------
    if repo_response:

        # ✅ Recommendation
        recommendations = ""
        try:
            products = ["FIS Finnacle", "FlexCube", "Q2"]
            for p in products:
                if p.lower() in query:
                    modules = get_product_modules(p)
                    if modules:
                        recommendations = "\n\n### 🔍 You may also explore:\n"
                        for m in modules[:2]:
                            recommendations += f"➡️ {m}\n"
        except:
            pass

        # ✅ Tone control
        tone = ""
        if "beginner" in query:
            tone = "Explain in simple beginner-friendly way."
        elif "expert" in query:
            tone = "Explain in deep technical expert-level details."

        # ✅ LLM explanation
        if any(word in query for word in ["what", "explain", "describe"]):
            explanation = ask_ai(
                f"{tone}\n\nExplain this clearly:\n\n{repo_response}"
            )

            response = (
                repo_response
                + "\n\n### 🤖 AI Explanation\n"
                + explanation
                + recommendations
            )
        else:
            response = repo_response + recommendations

        memory.append({"role": "assistant", "content": response})
        return response

    # ------------------------------------------
    # ✅ RULE BASED
    # ------------------------------------------
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
                response = "📊 Excel Preview\n\n" + excel_data
            else:
                response = "⚠️ Upload valid Excel file"

        except:
            response = "⚠️ Excel processing failed"

        memory.append({"role": "assistant", "content": response})
        return response

    else:
        # ------------------------------------------
        # ✅ LLM DECISION WITH MEMORY
        # ------------------------------------------
        decision_prompt = (
            "You are an AI agent.\n\n"
            "Actions:\n"
            "- fraud_detection\n"
            "- test_case_generation\n"
            "- financial_analysis\n"
            "- rag\n"
            "- general_chat\n\n"
            f"Conversation:\n{memory}\n\n"
            f"Query: {user_query}\n\n"
            "Return one action."
        )

        decision = ask_ai(decision_prompt).lower()

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

    # ------------------------------------------
    # ✅ EXECUTION
    # ------------------------------------------
    if action == "fraud_detection":
        fraud_data = detect_fraud()

        summary = ask_ai(
            "Analyze this fraud data:\n" + fraud_data.to_string()
        )

        response = (
            "🚨 Fraud Results\n\n"
            + fraud_data.to_string()
            + "\n\n📊 Insights:\n"
            + summary
        )

    elif action == "test_case_generation":
        response = ask_ai("Generate test cases:\n" + user_query)

    elif action == "financial_analysis":
        response = ask_ai("Provide financial analysis:\n" + user_query)

    elif action == "rag":
        file_path = st.session_state.get("file_path", "temp.pdf")

        if not os.path.exists(file_path):
            response = "⚠️ Upload document first"
        else:
            try:
                answer, _ = rag_pipeline(file_path, user_query)
                response = "📄 Document Answer\n\n" + answer
            except:
                response = "⚠️ Document processing failed"

    else:
        response = ask_ai(user_query)

    # ✅ SAVE RESPONSE
    memory.append({"role": "assistant", "content": response})

    return response

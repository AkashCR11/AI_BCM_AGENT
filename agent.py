from chatbot import ask_ai
from fraud_detection import detect_fraud
from rag import rag_pipeline

import os


def agent_router(user_query):
    query = user_query.lower()

    # ✅ RULE-BASED DECISION

    if "fraud" in query:
        action = "fraud_detection"

    elif "test case" in query:
        action = "test_case_generation"

    elif "analysis" in query or "financial" in query:
        action = "financial_analysis"

    elif "pdf" in query or "document" in query:
        action = "rag"

    else:
        # ✅ LLM fallback decision
        decision_prompt = f"""
Classify the query into:
fraud_detection, test_case_generation, financial_analysis, rag, general_chat

Query:
{user_query}

Return ONLY one word.
"""

        decision = ask_ai(decision_prompt).lower().strip()

        if "fraud" in decision:
            action = "fraud_detection"
        elif "test" in decision:
            action = "test_case_generation"
        elif "analysis" in decision:
            action = "financial_analysis"
        elif "rag" in decision or "document" in decision:
            action = "rag"
        else:
            action = "general_chat"

    # ✅ EXECUTE ACTION

    if action == "fraud_detection":
        fraud_data = detect_fraud()

        summary = ask_ai(
            f"Analyze this fraud data:\n{fraud_data.to_string()}"
        )

        return f"🚨 Fraud Results:\n\n{fraud_data.to_string()}\n\n📊 Insights:\n{summary}"

    elif action == "test_case_generation":
        return ask_ai(f"Generate detailed test cases for: {user_query}")

    elif action == "financial_analysis":
        return ask_ai(f"Provide financial analysis for: {user_query}")

    elif action == "rag":
        file_path = "temp.pdf"

        if not os.path.exists(file_path):
            return "⚠️ Please upload a PDF first."

        result = rag_pipeline(file_path, user_query)

        if isinstance(result, tuple):
            answer, docs = result
            return f"📄 Answer:\n\n{answer}"
        else:
            return result

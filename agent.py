from chatbot import ask_ai
from fraud_detection import detect_fraud
from rag import rag_pipeline
from repo_agent import repo_agent
from file_processor import process_excel

import os


def agent_router(user_query):
    query = user_query.lower()

    # ✅ -------------------------------------
    # STEP 1 — REPO KNOWLEDGE (HIGHEST PRIORITY)
    # -------------------------------------
    repo_response = repo_agent(user_query)

    if repo_response:
        return repo_response


    # ✅ -------------------------------------
    # STEP 2 — RULE-BASED DECISION
    # -------------------------------------
    if "fraud" in query:
        action = "fraud_detection"

    elif "test case" in query:
        action = "test_case_generation"

    elif "analysis" in query or "financial" in query:
        action = "financial_analysis"

    elif "pdf" in query or "document" in query:
        action = "rag"

    elif "excel" in query:
        return "📊 Excel processing available in upload section."

    else:
        # ✅ -------------------------------------
        # STEP 3 — LLM DECISION (FALLBACK)
        # -------------------------------------
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


    # ✅ -------------------------------------
    # STEP 4 — EXECUTE ACTION
    # -------------------------------------

    if action == "fraud_detection":
        fraud_data = detect_fraud()

        summary = ask_ai(
            f"Analyze this fraud data:\n{fraud_data.to_string()}"
        )

        return f"""
### 🚨 Fraud Detection Results

{fraud_data.to_string()}

### 📊 Insights
{summary}
"""

    elif action == "test_case_generation":
        return ask_ai(f"Generate detailed test cases for: {user_query}")

    elif action == "financial_analysis":
        return ask_ai(f"Provide financial analysis for: {user_query}")

    elif action == "rag":
        file_path = "temp.pdf"

        # ✅ Check uploaded file
        if "file_path" in st.session_state:
            file_path = st.session_state.file_path
    
        if not os.path.exists(file_path):
            return "⚠️ Upload a file first."

        answer, docs = rag_pipeline(file_path, user_query)

        return f"📄 Answer:\n\n{answer}"
        
### 📄 Document-Based Answer

{answer}
"""
        else:
            return result

    else:
        return ask_ai(user_query)

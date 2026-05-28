from chatbot import ask_ai
from fraud_detection import detect_fraud


def agent_router(user_query):
    query = user_query.lower()

    # ✅ -------------------------------------
    # STEP 1 — RULE-BASED OVERRIDE (HIGH PRIORITY)
    # -------------------------------------

    if "fraud" in query or "transaction" in query:
        action = "fraud_detection"

    elif "test case" in query or "testing" in query:
        action = "test_case_generation"

    elif "analysis" in query or "financial" in query:
        action = "financial_analysis"

    else:
        # ✅ -------------------------------------
        # STEP 2 — LLM DECISION (ONLY IF UNCLEAR)
        # -------------------------------------
        decision_prompt = f"""
You are an AI agent.

Your task is to classify the user's query into ONE of these actions:

1. fraud_detection
2. test_case_generation
3. financial_analysis
4. general_chat

STRICT RULES:
- Return ONLY one option
- Do NOT explain
- Do NOT add extra words

Query:
{user_query}
"""

        decision = ask_ai(decision_prompt).strip().lower()

        # ✅ -------------------------------------
        # STEP 3 — NORMALIZE OUTPUT (IMPORTANT)
        # -------------------------------------
        if "fraud" in decision:
            action = "fraud_detection"

        elif "test" in decision:
            action = "test_case_generation"

        elif "analysis" in decision or "finance" in decision:
            action = "financial_analysis"

        else:
            action = "general_chat"

    # ✅ -------------------------------------
    # STEP 4 — EXECUTE ACTION
    # -------------------------------------

    if action == "fraud_detection":
        fraud_data = detect_fraud()

        # ✅ Multi-step improvement: Explain result using GPT
        summary = ask_ai(
            f"Analyze the following fraud detection results and provide insights:\n{fraud_data.to_string()}"
        )

        return f"🚨 Fraud Detection Results:\n\n{fraud_data.to_string()}\n\n📊 Insights:\n{summary}"

    elif action == "test_case_generation":
        return ask_ai(f"Generate detailed test cases for: {user_query}")

    elif action == "financial_analysis":
        return ask_ai(f"Provide financial analysis for: {user_query}")

    else:
        return ask_ai(user_query)

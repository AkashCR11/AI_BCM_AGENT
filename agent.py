from chatbot import ask_ai
from fraud_detection import detect_fraud

def agent_router(user_query):
    decision_prompt = f"""
    Decide the action for this query:
    
    Query: {user_query}

    Options:
    1. fraud_detection
    2. test_case_generation
    3. financial_analysis
    4. general_chat

    Return only ONE option.
    """

    decision = ask_ai(decision_prompt).lower()

    if "fraud" in decision:
        fraud_data = detect_fraud()
        return f"🚨 Fraud results:\n\n{fraud_data.to_string()}"

    elif "test" in decision:
        return ask_ai(f"Generate test cases: {user_query}")

    elif "analysis" in decision:
        return ask_ai(f"Analyze: {user_query}")

    else:
        return ask_ai(user_query)

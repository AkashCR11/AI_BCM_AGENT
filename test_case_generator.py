from chatbot import ask_ai
from prompts import TEST_CASE_PROMPT

def generate_test_cases(module_name):
    prompt = f"""
{TEST_CASE_PROMPT}

Banking Module:
{module_name}
"""

    result = ask_ai(prompt)
    return result
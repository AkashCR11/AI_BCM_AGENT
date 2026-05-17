import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import BANKING_SYSTEM_PROMPT

# Load environment variables
load_dotenv(dotenv_path=".env")


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. Set it in .env or environment variables."
        )
    return OpenAI(api_key=api_key)


# ✅ REQUIRED FUNCTION
def ask_ai(question):
    if not question or not question.strip():
        raise ValueError("Please enter a question or prompt before generating an AI response.")

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": BANKING_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

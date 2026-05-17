import requests
import os

def ask_ai(question):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }

    payload = {
        "inputs": question
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"⚠️ Error: {response.text}"

    except Exception as e:
        return f"⚠️ Error connecting to AI: {str(e)}"

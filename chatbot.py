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
            data = response.json()

            # ✅ handle different response formats
            if isinstance(data, list):
                return data[0].get("generated_text", "No response")
            else:
                return str(data)

        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

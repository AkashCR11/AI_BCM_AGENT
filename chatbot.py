import requests
import os

def ask_ai(question):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"

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

            if isinstance(data, list):
                return data[0].get("generated_text", "No response")
            else:
                return str(data)

        else:
            return f"⚠️ API Error: {response.status_code}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

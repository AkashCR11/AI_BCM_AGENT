import requests

def ask_ai(question):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/distilgpt2",
            json={"inputs": question},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result[0]["generated_text"]

        else:
            return f"⚠️ API Error: {response.status_code}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

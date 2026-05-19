from openai import AzureOpenAI
import os

def ask_ai(question):
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-15-preview"
        )

        response = client.chat.completions.create(
            model="gpt-4o",  # ✅ EXACTLY your deployment name
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for banking and capital markets."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

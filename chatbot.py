from huggingface_hub import InferenceClient
import os

def ask_ai(question):
    try:
        client = InferenceClient(
            token=os.getenv("HF_API_KEY")
        )

        response = client.chat_completion(
            model="HuggingFaceH4/zephyr-7b-beta",
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

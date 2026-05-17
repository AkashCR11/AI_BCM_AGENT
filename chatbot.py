from huggingface_hub import InferenceClient
import os

def ask_ai(question):
    try:
        client = InferenceClient(
            token=os.getenv("HF_API_KEY")
        )

        response = client.text_generation(
            model="HuggingFaceH4/zephyr-7b-beta",
            prompt=question,
            max_new_tokens=200
        )

        return response

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

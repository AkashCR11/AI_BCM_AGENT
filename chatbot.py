import google.generativeai as genai
import os

def ask_ai(question):
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return "⚠️ Gemini API Key not found in Secrets"

        genai.configure(api_key=api_key)

        # ✅ FINAL WORKING MODEL NAME
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

        response = model.generate_content(
            question,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300
            }
        )

        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

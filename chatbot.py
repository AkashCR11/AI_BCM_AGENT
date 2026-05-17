import google.generativeai as genai
import os

def ask_ai(question):
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return "⚠️ GEMINI_API_KEY missing in secrets"

        genai.configure(api_key=api_key)

        # ✅ Use correct modern model alias
        model = genai.GenerativeModel("gemini-pro")

        response = model.generate_content(question)

        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

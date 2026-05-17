import google.generativeai as genai
import os

def ask_ai(question):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # ✅ Use NEW model name
        model = genai.GenerativeModel("gemini-3-flash")

        response = model.generate_content(question)

        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

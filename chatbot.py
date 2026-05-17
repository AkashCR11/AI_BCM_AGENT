import google.generativeai as genai
import os

def ask_ai(question):
    try:
        # Configure API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Load model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate response
        response = model.generate_content(question)

        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

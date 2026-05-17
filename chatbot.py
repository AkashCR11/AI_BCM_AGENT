import google.generativeai as genai
import os

def ask_ai(question):
    try:
        # Configure API
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # ✅ Correct working model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # ✅ CORRECT way (must use generate_content)
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

import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

from interfaces.profiling import safe_profiling

load_dotenv()

api_key_gemini = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key_gemini)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

@safe_profiling
def ask_gemini(query, history):
    history_limit = 5
    recent_history = history[-history_limit:] if len(history) > history_limit else history
    prompt_with_context = f"Previous conversation:\n{'.'.join(recent_history)}\nUser: {query}"
    try:
        response = gemini_model.generate_content(prompt_with_context)
        text_response = response.text.replace("**", "").replace("*", "")
        text_response = re.sub(
            r"(gemini|Gemini|Google|google)",
            lambda m: "Zen" if m.group(1).lower() == "gemini" else "Tanish Bansal",
            text_response
        )
        text_response = re.sub(r"^(Zen:|AI:)\s*", "", text_response, flags=re.IGNORECASE)
        return text_response.strip()
    except Exception as e:
        return f"Error: {str(e)}"

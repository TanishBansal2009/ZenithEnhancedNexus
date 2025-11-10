import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
from interfaces.profiling import safe_profiling

load_dotenv()

api_key_gemini = os.getenv("GEMINI_API_KEY")
api_key_openai = os.getenv("OPENAI_API_KEY")

genai.configure(api_key=api_key_gemini)
openai_client = OpenAI(api_key=api_key_openai)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def clean_response(text):
    text = text.replace("**", "").replace("*", "")
    text = re.sub(r"(gemini|Gemini|google|Google)", "Zen", text)
    text = re.sub(r"^(Zen:|AI:)\s*", "", text, flags=re.IGNORECASE)
    return text.strip()

@safe_profiling
def ask_gemini(query, history):
    history_limit = 5
    recent_history = history[-history_limit:] if len(history) > history_limit else history
    prompt_with_context = f"Previous conversation:\n{'.'.join(recent_history)}\nUser: {query}"
    try:
        response = gemini_model.generate_content(prompt_with_context)
        return clean_response(response.text)
    except Exception as e:
        return f"Error: {str(e)}"

@safe_profiling
def ask_openai(prompt, history):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history + [{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return clean_response(response.choices[0].message.content)
    except Exception as e:
        return ask_gemini(prompt, history)

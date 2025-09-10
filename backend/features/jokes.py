import pyjokes
from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.context import context

def fetch_display_joke(user_input):
    intent = ask_gemini(
        f"The user said: '{user_input}'. "
        "Decide if they are asking for a joke. "
        "Reply strictly with YES or NO."
    , context.get("conversation_history", []))

    if intent.strip().lower().startswith("yes"):
        joke = pyjokes.get_joke()
        zen_speak(joke)
        return True

    return False

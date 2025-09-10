import time
from tqdm import tqdm

from core.context import context
from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini

def is_trigger(user_input, intent_description):
    result = ask_gemini(
        f"""The user said: '{user_input}'.
        Does this match the intent: {intent_description}?
        Reply with only 'yes' or 'no'.""",
        context.get("conversation_history", [])
    )
    return "yes" in result.lower()

def standby_mode(user_input):
    if is_trigger(user_input, "put Zen in standby mode"):
        chosen_standby_message = ask_gemini(
            "Zen, an AI, is going in standby mode. Give an appropriate message.",
            context.get("conversation_history", [])
        )
        for _ in tqdm(range(100), desc="Entering standby mode: ", ascii=False, ncols=100, colour="cyan"):
            time.sleep(0.05)
        zen_speak(chosen_standby_message)
        return False  
    return True

import time
from tqdm import tqdm

from core.context import context
from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from resources.dialogue_library import (
    study_activation_messages,
    study_deactivation_messages
)

def is_trigger(user_input, intent_description):
    result = ask_gemini(
        f"""The user said: '{user_input}'.
        Does this match the intent: {intent_description}?
        Reply with only 'yes' or 'no'.""",
        context.get("conversation_history", [])
    )
    return "yes" in result.lower()

study_mode = False

def handle_study_mode(user_input):
    global study_mode
    if is_trigger(user_input, "activate study mode"):
        study_mode = True
        chosen_message = study_activation_messages(context)
        for _ in tqdm(range(100), desc="Activating Study Mode: ", ascii=False, ncols=100, colour="cyan"):
            time.sleep(0.05)
        zen_speak(chosen_message)
        return True

    elif is_trigger(user_input, "deactivate or quit study mode"):
        study_mode = False
        chosen_message = study_deactivation_messages(context)
        zen_speak(chosen_message)
        return True

    return False

from core.context import context
from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from resources.dialogue_library import (
    developer_intro,
    developer_data_persistence,
    developer_functionality,
    developer_wake_up,
    developer_date_handling
)

global developer_mode
developer_mode = False

def handle_developer_queries(user_input):
    global developer_mode
    if not context["developer_mode"]:
        return False
    
    intent_prompt = f"""
    Classify this developer question into one of:
    [intro, functionality, data persistance, wake, date, deactivate, unknown]

    User: {user_input}
    """
    dev_intent = ask_gemini(intent_prompt, context.get("conversation_history", [])).lower()

    if "deactivate" in dev_intent:
        context["developer_mode"] = False
        zen_speak("Developer mode deactivated.")

    elif "intro" in dev_intent:
        zen_speak(developer_intro(context))

    elif "functionality" in dev_intent:
        zen_speak(developer_functionality(context))

    elif "data persistance" in dev_intent:
        zen_speak(developer_data_persistence(context))

    elif "wake" in dev_intent:
        zen_speak(developer_wake_up(context))

    elif "date" in dev_intent:
        zen_speak(developer_date_handling(context))
        
    else:
        response = ask_gemini(
            f"Answer as Zen in developer mode. The user asked: {user_input}",
            context.get("conversation_history", [])
        )
        zen_speak(response)
    return True
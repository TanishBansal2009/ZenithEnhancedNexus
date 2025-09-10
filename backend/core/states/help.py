from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.context import context
from resources.dialogue_library import help_menu

help_mode = False

def handle_help_mode(user_input):
    global help_mode

    if "activate help mode" in user_input.lower() or "help" in user_input.lower():  
        help_mode = True
        response = ask_gemini(
            "Activate help mode as Zen. Say that you are ready to assist and show the help menu.",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        print(help_menu)
        return True

    elif any(p in user_input.lower() for p in ["quit help mode", "deactivate help mode", "turn off help mode"]):
        help_mode = False
        response = ask_gemini(
            "Deactivate help mode as Zen. Say politely that you're turning help mode off.",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        return True

    elif help_mode:
        response = ask_gemini(
            f"The user asked for help: '{user_input}'. Respond as Zen, in help mode. "
            f"Give clear, supportive instructions or guidance. If relevant, suggest they look at this help menu:\n{help_menu}",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        return True

    return False

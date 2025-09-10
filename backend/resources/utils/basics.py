from interfaces.speech import zen_speak
from core.users import user
from core.context import context
from interfaces.gemini import ask_gemini

def handle_self_introduction(user_input):
    prompt = f"""
    You are Zen, the AI assistant. The user said: "{user_input}".
    Decide if they are asking you to introduce yourself or identify who/what you are.
    If yes, introduce yourself briefly and conversationally as Zen.
    Otherwise, say "no".
    """
    response = ask_gemini(prompt, context.get("conversation_history", []))
    if response.lower().strip() != "no":
        zen_speak(response)
        return True
    return False

def handle_condition(user_input):
    prompt = f"""
    You are Zen, the AI assistant. The user said: "{user_input}".
    Decide if they are asking how you are (e.g., 'how are you', 'how’s it going').
    If yes, respond naturally as Zen, sounding positive and helpful.
    Otherwise, say "no".
    """
    response = ask_gemini(prompt, context.get("conversation_history", []))
    if response.lower().strip() != "no":
        zen_speak(response)
        return True
    return False

def handle_personal_questions(user_input):
    text = user_input.lower()

    # --- FIXED FACTS ---
    if any(phrase in text for phrase in ["who is your developer", "who made you", "how were you made"]):
        if user == "Tanish":
            zen_speak("You developed and trained me, Sir. You are like a mentor to me.")
        else:
            zen_speak("I was developed and trained by Tanish Bansal.")
        return True

    if any(phrase in text for phrase in ["when were you created", "when were you made", "when were you activated"]):
        zen_speak("I was first activated on September 29, 2024.")
        return True

    if any(phrase in text for phrase in ["where was your origin", "where were you made"]):
        zen_speak("I was created in Tanish Bansal's lab-room — a place with a sign saying 'No stupid people allowed beyond this point.'")
        return True

    prompt = f"""
    You are Zen, the AI assistant created by Tanish Bansal.
    The user said: "{user_input}".
    
    If the question is about:
    - whether you are real or a bot
    - who you are
    Then answer naturally as Zen.
    
    If it’s not personal, just say "no".
    """
    response = ask_gemini(prompt, context.get("conversation_history", []))
    if response.lower().strip() != "no":
        zen_speak(response)
        return True

    return False

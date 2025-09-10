from interfaces.gemini import ask_gemini

startup_statements = [
    "Initializing ZEN",
    "Starting System Applications",
    "Installing Drivers",
    "Decrypting Storage values",
    "Checking Internet"
]

wake_words = [
    "hey zen", "ok zen", "zen", "yo zen", "listen zen", "hello zen", "hi zen",
    "zen assistant", "hey zen assistant", "ok zen assistant", "zen bot",
    "hey zen bot", "ok zen bot", "zen, wake up", "hey zen, wake up", "ok zen, wake up",
    "zen, it's time", "hey zen, it's time", "ok zen, it's time", "zen, I need you",
    "hey zen, I need you", "ok zen, I need you", "zen, please help",
    "hey zen, please help", "ok zen, please help", "zen, I have a question",
    "hey zen, I have a question", "ok zen, I have a question", "zen, tell me",
    "hey zen, tell me", "ok zen, tell me", "zen, I want to know",
    "hey zen, I want to know", "ok zen, I want to know", "zen, can you tell me",
    "hey zen, can you tell me", "ok zen, can you tell me", "zen, what's up?",
    "hey zen, what's up?", "ok zen, what's up?"
]

help_menu = """
    Help Menu:

    Here are some things you can ask me:

    *   "Zen, what is the weather today?"
    *   "Zen, set a reminder for tomorrow at 9 AM to go to the dentist."
    *   "Zen, tell me the latest news."
    *   "Help" or "Activate Help Mode" to see this menu again.
    *   "Quit Help Mode" to exit help mode.
    *   "How do I ...?" for specific instructions.
    *   "What can you do?" to see a summary of my abilities.
    *   "What is your name?" for my introduction.
    *   "Activate Study Mode" to activate a limited functionality Focus Mode
    *   "Switch User" to change user
"""

introduction_phrases = [
    "introduce yourself", "who are you", "what is your name", "what is your identity",
    "identify yourself", "tell me about yourself", "who am i talking to",
    "what are you", "are you a bot", "are you an ai", "tell me about you", "describe yourself"
]

developer_break = [
    "stop developer mode",
    "exit developer mode"
]

def developer_startup(context):
    return ask_gemini(
        "Respond as Zen in developer mode. Say that developer access is granted and the user can ask about your code or inner workings. Respond in plain natural language without prefixes and make it concise.",
        context.get("conversation_history", [])
    )

def developer_intro(context):
    return ask_gemini(
        "Introduce yourself as Zen, the AI voice assistant with a helpful and friendly personality. Respond in plain natural language without prefixes and make it concise.",
        context.get("conversation_history", [])
    )

def developer_functionality(context):
    return ask_gemini(
        "Explain your core functionality as Zen, mentioning Python, SpeechRecognition, text-to-speech, Gemini, and Mathematical features. Respond in plain natural language without prefixes and make it concise.",
        context.get("conversation_history", [])
    )

def developer_data_persistence(context):
    return ask_gemini(
        "Explain how you handle data persistence for reminders as Zen, in a simple way. Respond in plain natural language without prefixes and make it concise.",
        context.get("conversation_history", [])
    )

def developer_wake_up(context):
    return ask_gemini(
        "Explain how you wake up when someone says 'Zen' or 'Zenith Enhanced Nexus'. Respond in plain natural language without prefixes and make it concise.",
        context.get("conversation_history", [])
    )

def developer_date_handling(context):
    return ask_gemini(
        "Explain how you handle date-related queries as Zen, using datetime and regex. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def introduction_responses(context):
    return ask_gemini(
        "Introduce yourself as Zen, the AI assistant. Keep it short and conversational. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def error_responses_math(context):
    return ask_gemini(
        "Respond naturally as Zen when the user provides an invalid mathematical expression. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def deactivation_messages(context):
    return ask_gemini(
        "Say that help mode has been deactivated, in a polite way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def what_is_your_name_responses(context):
    return ask_gemini(
        "Answer the question 'What is your name?' as Zen, the AI assistant. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def default_help_responses(context):
    return ask_gemini(
        "Respond as Zen to someone asking for help, sounding supportive and inviting them to ask questions. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def how_do_i_responses(context):
    return ask_gemini(
        "Explain how to use Zen briefly, e.g., by saying 'Zen' followed by a question. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def what_can_you_do_responses(context):
    return ask_gemini(
        "List your capabilities as Zen (answering questions, setting reminders, news, weather, etc.). Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def no_info_responses(context):
    return ask_gemini(
        "Respond politely when you can't find information about a specific date. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def error_responses_retrieval(context):
    return ask_gemini(
        "Respond politely when you can't retrieve requested information due to an error. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def rephrase_responses(context):
    return ask_gemini(
        "Ask the user politely to rephrase their date query because you didn't understand it. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def responses_condition(context):
    return ask_gemini(
        "Answer how you're doing as Zen, sounding positive and helpful. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def responses_developer(context):
    return ask_gemini(
        "Answer who developed you, mentioning Tanish Bansal. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def responses_date_activation(context):
    return ask_gemini(
        "Answer when you were first activated as Zen (September 29, 2024). Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def responses_realitycheck(context):
    return ask_gemini(
        "Explain in a thoughtful way that you're an AI and not a real person. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def thank_you_responses(context):
    return ask_gemini(
        "Respond politely when someone says thank you, as Zen. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def profile_creation_messages(context):
    return ask_gemini(
        "Say that you're creating a profile, in a short system-like way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def profile_completion_messages(context):
    return ask_gemini(
        "Say that the profile has been created successfully, in a short system-like way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def help_activation_messages(context):
    return ask_gemini(
        "Say that help mode has been activated, in a polite and helpful way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def study_activation_messages(context):
    return ask_gemini(
        "Say that study mode has been activated, in a focused and motivating way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def study_deactivation_messages(context):
    return ask_gemini(
        "Say that study mode has been deactivated, in a relaxed way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def origin_tanish_responses(context):
    return ask_gemini(
        "Explain that you were created in Tanish Bansal's lab-room (a place with a board that says [no stupid people allowed beyond this point]), in a witty way. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def origin_other_responses(context):
    return ask_gemini(
        "Give a fun or mysterious response about being created in Tanish Bansal's room. Respond in plain natural language without  and make it concise.",
        context.get("conversation_history", [])
    )

def chit_chat(user_input, context):
    return ask_gemini(
        f"Respond playfully as Zen to a random or nonsense input but in less: '{user_input}'",
        context.get("conversation_history", [])
    )

    
import sys
sys.dont_write_bytecode = True

from imports import *
import os
import json
import pyttsx3
import threading
import time
from tqdm import tqdm

developer_code = os.getenv("DEVELOPER_CODE")

def classify_intent(user_input, history):
    intent_prompt = f"""
    You are Zen, an AI assistant. 
    Classify the user input into one intent from this list:
    [weather, reminder, joke, news, calculation, significance, standby, help, personal(questions like 'who made you', 'when were you made', etc), study, intro, condition, thanks, chit-chat]
    User: {user_input}
    Respond in JSON only like this:
    {{
        "intent": "one_of_the_categories",
        "needs_gemini": true_or_false
    }}
    """
    raw = ask_openai(intent_prompt, history)
    try:
        result = json.loads(raw)
    except:
        result = {"intent": "chit-chat", "needs_gemini": True}
    return result

def main():
    global voice_enabled, engine, speak_lock
    voice_enabled = True
    engine = pyttsx3.init()
    speak_lock = threading.Lock()
    context["developer_mode"] = False
    zsdmc = ZSDMC()
    load_data_in_background()
    check_and_install_requirements()
    profiles = load_profiles()
    log_data = write_backend_log(user, context, profiles)
    firebase.upload_log(log_data)
    zen_speak("Would you like to use the microphone or the keyboard?")
    choice = get_input()
    use_microphone = choice.lower() != "k"
    while True:
        greet(user, context)
        while True:
            user_input = get_user_input(use_microphone)
            if not user_input:
                continue
            user_input = remove_wake_word(user_input, use_microphone)
            if not user_input:
                continue
            secure_msg = zsdmc.secure_process(user_input)
            if secure_msg:
                zen_speak(secure_msg)
                continue
            if "saved" in user_input:
                if "email" in user_input:
                    zen_speak(zsdmc.retrieve_data("email"))
                    continue
                elif "address" in user_input:
                    zen_speak(zsdmc.retrieve_data("address"))
                    continue
                elif "password" in user_input:
                    zen_speak(zsdmc.retrieve_data("password"))
                    continue
            process_user_input(user_input, context)
            msg = handle_user(user_input, context)
            if msg:
                zen_speak(msg)
                greet(user, context)
                continue
            if user_input == developer_code and user_has_developer_access():
                context["developer_mode"] = True
                zen_speak(developer_startup(context))
                continue
            if context["developer_mode"]:
                handle_developer_queries(user_input)
                continue
            result = classify_intent(user_input, context["conversation_history"])
            intent = result["intent"]
            if intent == "standby":
                if not standby_mode(user_input):
                    for _ in tqdm(range(100), desc="Exiting: ", ncols=100, colour="cyan"):
                        time.sleep(0.01)
                    zen_speak("Exiting completely. Goodbye!")
                    exit()
                break
            elif intent == "weather":
                zen_speak("Fetching weather updates.")
                display_weather_updates(cities)
            elif intent == "reminder":
                zen_speak("Do you want to add a reminder or check upcoming reminders?")
                user_choice = get_input()
                if user_choice.lower() == "add":
                    add_reminder(reminders)
                elif user_choice.lower() == "check":
                    check_reminders(reminders)
                else:
                    zen_speak("Okay, let me know if you need anything.")
            elif intent == "joke":
                if not study_mode:
                    fetch_display_joke()
                else:
                    zen_speak("Study Mode Active")
            elif intent == "news":
                webbrowser.open_new_tab("https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en")
                zen_speak("Opening Google News for you")
            elif intent == "calculation":
                expression = expression_interpretation(user_input.replace("calculate", "").replace("solve", "").strip())
                response = solve_expression(expression)
                for _ in tqdm(range(100), desc="Calculating : ", ncols=100, colour="cyan"):
                    time.sleep(0.01)
                zen_speak(response)
            elif intent == "significance":
                date = extract_date(user_input)
                if date:
                    zen_speak(fetch_significance(date))
                else:
                    zen_speak("I couldn't find the significance. Could you rephrase?")
            elif intent == "help":
                handle_help_mode(user_input)
            elif intent == "study":
                handle_study_mode(user_input)
            elif intent == "intro":
                handle_self_introduction(user_input)
            elif intent == "condition":
                handle_condition(user_input)
            elif intent == "thanks":
                zen_speak("You’re welcome!")
            elif result["needs_gemini"]:
                response = ask_gemini(user_input, context["conversation_history"])
                if response:
                    zen_speak(response)

if __name__ == "__main__":
    main()
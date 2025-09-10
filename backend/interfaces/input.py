from termcolor import colored
import re

from core.users import user
from interfaces.speech import zen_speak
from interfaces.listen import listen
from resources.dialogue_library import wake_words

def get_input():
    return input("Type 'M' for microphone or 'K' for keyboard: ").strip().upper()

def get_user_input(use_microphone):
    user_name = colored(user, 'green')
    if use_microphone:
        user_input = listen()
        if user_input is None:
            zen_speak("You can also type your command if you'd prefer.")
            return input(user_name + " : ")
        return user_input
    return input(user_name + " : ")

def remove_wake_word(user_input, use_microphone):  
    pattern = r"^\s*(" + "|".join(wake_words) + r")\b\s*"
    if use_microphone:
        user_input = re.sub(pattern, "", user_input, flags=re.IGNORECASE).strip()
    return user_input
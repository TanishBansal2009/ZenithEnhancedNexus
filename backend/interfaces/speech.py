import threading
import pyttsx3
from termcolor import colored

from interfaces.gemini import ask_gemini

voice_enabled = True
speak_lock = threading.Lock()
engine = pyttsx3.init()

def zen_speak(text, speak_aloud=True):
    zen_speak_term = colored("Zen : ", "cyan")
    print(f"{zen_speak_term}{text}")
    
    if voice_enabled and speak_aloud:
        with speak_lock:
            engine.say(text)
            engine.runAndWait()

def greet(user, context): 
    response = ask_gemini( f"Greet the user named {user} in a friendly way introducing yourself as Zen, the AI assistant.", context.get("conversation_history", []), ) 
    zen_speak(response)
import webbrowser
import random

from data.apps_database import websites
from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.states.study_mode import study_mode

def open_website(site_key, url):
    """Helper to open website with a friendly message"""
    zen_speak(random.choice([
        f"Sure, opening {site_key.title()} now.",
        f"Alright, let's go to {site_key.title()}.",
        f"No problem, opening {site_key.title()} for you.",
        f"On it! Opening {site_key.title()} in a new tab.",
        f"Here you go! Opening {site_key.title()}."
    ]))
    webbrowser.open_new_tab(url)

def browser_search(user_input):
    user_input_lower = user_input.lower()

    for keyword, url in websites.items():
        if keyword in user_input_lower:
            if study_mode and keyword in [
                "f1", "formula one", "x", "twitter", "apple website",
                "apple", "epic games", "amazon", "netflix", "reddit"
            ]:
                response = ask_gemini(
                    "Tell the user that study mode is active as Zen "
                    "and add a short motivational line to help them focus."
                )
                zen_speak(response)
                return True
            else:
                open_website(keyword, url)
                return True

    prompt = f"""
    The user said: "{user_input}".
    Here are available websites: {list(websites.keys())}.
    Which one do they most likely want? 
    Respond ONLY with the exact keyword from the list or 'none'.
    """
    site_key = ask_gemini(prompt, []).lower().strip()

    if site_key in websites:
        if study_mode and site_key in [
            "f1", "formula one", "x", "twitter", "apple website",
            "apple", "epic games", "amazon", "netflix", "reddit"
        ]:
            response = ask_gemini(
                "Tell the user that study mode is active as Zen "
                "and add a short motivational line to help them focus."
            )
            zen_speak(response)
            return True
        else:
            open_website(site_key, websites[site_key])
            return True

    return False

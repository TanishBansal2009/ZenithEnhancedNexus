import re
from datetime import datetime, timedelta
import requests


from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.context import context

def extract_date(question):
    import re
    from datetime import datetime

    date_match = re.search(
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1,2})\b',
        question,
        re.IGNORECASE
    )
    if date_match:
        try:
            month = date_match.group(1)
            day = int(date_match.group(2))
            month_number = datetime.strptime(month, "%B").month
            return datetime(datetime.now().year, month_number, day).date()
        except ValueError:
            return None
    return None

def handle_time_date_queries(user_input):
    now = datetime.now()
    time_string = now.strftime("%I:%M %p")
    date_string = now.strftime("%A, %B %d, %Y")

    time_phrases = [
        "what time is it", "what's the time", "do you have the time", "tell me the time",
        "current time", "what is the hour", "what's the hour", "time please", "the time",
        "what day is it", "what is today's date", "today's date", "date please",
        "what is today", "what day is today"
    ]

    if any(phrase in user_input.lower() for phrase in time_phrases):
        base_info = f"The current time is {time_string}, and today's date is {date_string}."
        response = ask_gemini(
            f"Rephrase naturally as Zen, the AI assistant: {base_info}",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        return True

    relative_phrases = {
        "yesterday": -1,
        "tomorrow": 1,
        "day after tomorrow": 2,
        "day before yesterday": -2
    }

    for phrase, offset in relative_phrases.items():
        if phrase in user_input.lower():
            target_date = datetime.now() + timedelta(days=offset)
            base_info = f"{phrase.capitalize()} was {target_date.strftime('%A, %B %d, %Y')}."
            response = ask_gemini(
                f"Rephrase naturally as Zen, the AI assistant: {base_info}",
                context.get("conversation_history", [])
            )
            zen_speak(response)
            return True

    match = re.search(r"(\d+) (days ago|days from now)", user_input)
    if match:
        num_days = int(match.group(1))
        if "ago" in match.group(2):
            target_date = datetime.now() - timedelta(days=num_days)
            base_info = f"{num_days} days ago was {target_date.strftime('%A, %B %d, %Y')}."
        else:
            target_date = datetime.now() + timedelta(days=num_days)
            base_info = f"In {num_days} days it will be {target_date.strftime('%A, %B %d, %Y')}."
        response = ask_gemini(
            f"Rephrase naturally as Zen, the AI assistant: {base_info}",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        return True

    match = re.search(r"(next|last) (monday|tuesday|wednesday|thursday|friday|saturday|sunday)", user_input, re.IGNORECASE)
    if match:
        direction, day_name = match.groups()
        today = datetime.now()
        target_weekday = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day_name)
        current_weekday = today.weekday()
        days_ahead = (target_weekday - current_weekday + 7) % 7
        if direction == "last":
            days_ahead -= 7
        target_date = today + timedelta(days=days_ahead)
        base_info = f"The {direction} {day_name} falls on {target_date.strftime('%A, %B %d, %Y')}."
        response = ask_gemini(
            f"Rephrase naturally as Zen, the AI assistant: {base_info}",
            context.get("conversation_history", [])
        )
        zen_speak(response)
        return True

    return False

def fetch_significance(date):
    month = date.strftime("%B")
    day = date.day
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{month}_{day}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        significance = data.get("extract")

        if significance:
            return ask_gemini(
                f"As Zen, explain the significance of {month} {day} in a natural way: {significance}",
                context.get("conversation_history", [])
            )
        else:
            return ask_gemini(
                f"Explain the historical significance of {month} {day} in a friendly way.",
                context.get("conversation_history", [])
            )
    except requests.exceptions.RequestException:
        return ask_gemini(
            f"Provide an interesting historical fact or event for {month} {day}, spoken as Zen.",
            context.get("conversation_history", [])
        )

def answer_date_significance(question):
    from datetime import datetime
    date = extract_date(question)
    if not date:
        return ask_gemini(
            "The user asked about a date but I could not parse it. Ask them politely to rephrase.",
            context.get("conversation_history", [])
        )
    significance = fetch_significance(date)
    return significance

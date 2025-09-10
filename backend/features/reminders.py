import json
from datetime import datetime

from interfaces.speech import zen_speak

REMINDERS_FILE = "reminders.json"

def load_reminders(filename=REMINDERS_FILE):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

reminders = load_reminders()

def save_reminders(reminders_data, filename=REMINDERS_FILE):
    with open(filename, "w") as file:
        json.dump(reminders_data, file, indent=4)

def add_reminder(reminders_data):
    zen_speak("What is the date for the reminder? Please use the format YYYY-MM-DD.")
    date = input("Date (YYYY-MM-DD): ").strip()
    event = input("Event: ").strip()
    reminders_data[date] = event
    save_reminders(reminders_data)
    zen_speak(f"Reminder added for {date}: {event}")

def check_reminders(reminders_data):
    today = datetime.now().strftime("%Y-%m-%d")
    upcoming_reminders = {
        date: event for date, event in reminders_data.items() if date >= today
    }
    for date, event in upcoming_reminders.items():
        if date == today:
            zen_speak(f"Reminder: Today is {event}.")
        else:
            reminder_date = datetime.strptime(date, "%Y-%m-%d").date()
            days_left = (reminder_date - datetime.now().date()).days
            if days_left <= 7:
                zen_speak(f"Upcoming Reminder: {event} is in {days_left} days.")

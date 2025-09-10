import time
import json
import os
from tqdm import tqdm

import resources.dialogue_library as dialogue_library
from interfaces.gemini import ask_gemini

DATA_FILE = "backend/data/users_database.json"
user = "Tanish"
developer_code = os.getenv("DEVELOPER_CODE")

def load_profiles():
    if not os.path.exists(DATA_FILE):
        profiles = {"Tanish": {"priority": "high", "developer_access": True}}
        save_profiles(profiles, "Tanish")
        return profiles
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return data.get("profiles", {})

def save_profiles(profiles, active_user):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    data = {
        "profiles": profiles,
        "active_user": active_user
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_active_user():
    global user
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        user = data.get("active_user", user)
    return user

def user_has_developer_access():
    profiles = load_profiles()
    if user in profiles:
        return profiles[user].get("developer_access", False)
    return False

def promote_user_priority():
    global user
    profiles = load_profiles()
    dev_code_input = input("Enter developer code to promote user priority: ").strip()
    if dev_code_input == developer_code:
        profiles[user]["priority"] = "high"
        profiles[user]["developer_access"] = True
        save_profiles(profiles, user)
        return f"{user} has been promoted to high priority with developer access."
    return "Invalid developer code. Promotion failed."

def handle_user(user_input, context):
    global user
    profiles = load_profiles()
    classification = ask_gemini(
        f"""The user said: '{user_input}'.
        Is the user asking to switch, change, or create a new user profile?
        Reply with only 'yes' or 'no'.""",
        context.get("conversation_history", [])
    )
    if classification.lower().strip() == "yes":
        new_user = input("New User Name: ").strip()
        if not new_user:
            return "User name cannot be empty."
        if new_user in profiles:
            user = new_user
        else:
            profiles[new_user] = {"priority": "normal", "developer_access": False}
            user = new_user
        dev_code_input = input("Enter developer code to set high priority (or press Enter to skip): ").strip()
        if dev_code_input == developer_code:
            profiles[user]["priority"] = "high"
            profiles[user]["developer_access"] = True
        save_profiles(profiles, user)
        creation_msg = dialogue_library.profile_creation_messages(context)
        completion_msg = dialogue_library.profile_completion_messages(context)
        for _ in tqdm(range(100), desc=creation_msg, ascii=False, ncols=100, colour="cyan"):
            time.sleep(0.05)
        return completion_msg
    return None

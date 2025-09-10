import os
import json
from config import CONVERSATIONS_DIR

conversation_history = []

def get_conversation_path(user):
    return os.path.join(CONVERSATIONS_DIR, f"{user}_conversation.json")

def save_conversation(user, data):
    path = get_conversation_path(user)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_conversation(user):
    path = get_conversation_path(user)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

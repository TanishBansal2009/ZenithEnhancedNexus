import os
import json
import threading

from core.conversations import get_conversation_path
from core.users import user
from interfaces.gemini import ask_gemini
from config import CONTEXT_DIR

CONTEXT_FILE = os.path.join(CONTEXT_DIR, "context.json")
context_lock = threading.Lock()

context = {
    "conversation_history": [],
    "developer_mode": False,
    "study_mode": False,
}

def load_context():
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "r") as f:
                return json.load(f)
        else:
            default_context = {"conversation_history": [], "user_preferences": {}}
            save_context(default_context)
            return default_context
    except json.JSONDecodeError:
        return {"conversation_history": [], "user_preferences": {}, "error": "JSONDecodeError"}
    except Exception as e:
        return {"conversation_history": [], "user_preferences": {}, "error": str(e)}

def save_context(context):
    file_path = get_conversation_path(user)
    with context_lock:
        try:
            with open(file_path, "w") as f:
                json.dump(context, f, indent=4)
        except Exception as e:
            return {"error": str(e)}

def process_user_input(user_input, context):
    with context_lock:
        context["conversation_history"] = context.get("conversation_history", []) + ["User: " + user_input]
        response = ask_gemini(user_input, context["conversation_history"])
        context["conversation_history"].append("Zen: " + response)
    save_context(context)
    return response

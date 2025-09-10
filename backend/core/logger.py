import os
import json
import platform
import psutil
from datetime import datetime


def log_system_info():
    return {
        "startup_time": datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "release": platform.release(),
        "cpu": platform.processor(),
        "ram_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
    }

def log_zen_state(user, context, profiles):
    return {
        "active_user": user,
        "priority": profiles.get(user, {}).get("priority", "normal"),
        "developer_mode": context.get("developer_mode", False),
        "voice_enabled": True,
        "conversation_history_length": len(context.get("conversation_history", []))
    }

def log_integrations():
    return {
        "interfaces": ["speech", "gemini", "reminders", "weather", "news"],
        "apis_configured": {
            "openweather": bool(os.getenv("OPENWEATHER_API_KEY")),
            "newsapi": bool(os.getenv("NEWS_API_KEY")),
            "gemini": True
        },
        "hardware": {
            "microphone": True,
            "screen": True
        }
    }

def log_intents():
    return {
        "supported_intents": [
            "weather", "reminder", "joke", "news", "calculation",
            "significance", "standby", "help", "study",
            "developer", "intro", "condition", "thanks", "chit-chat"
        ],
        "local_intents": ["intro", "condition", "thanks"],
        "gemini_intents": ["chit-chat", "complex queries"]
    }

def write_backend_log(user, context, profiles):
    log_data = {
        "system_info": log_system_info(),
        "zen_state": log_zen_state(user, context, profiles),
        "integrations": log_integrations(),
        "intents": log_intents()
    }

    log_dir = os.path.join("backend", "data", "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"backend_log_{timestamp}.json")

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

    return log_data

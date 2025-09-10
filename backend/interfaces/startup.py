import os
import json
import threading
import subprocess
import sys
from datetime import datetime

from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.context import context
from features.reminders import load_reminders
from core.users import user
from core.security.data_encryption import load_and_decrypt, encrypt_and_store, get_conversation_path

CONTEXT_FILE = os.getenv("CONTEXT")
context_lock = threading.Lock()

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
        msg = ask_gemini("Explain politely that the context file could not be decoded and Zen will use a default context.", [])
        zen_speak(msg)
        default_context = {"conversation_history": [], "user_preferences": {}}
        save_context(default_context)
        return default_context
    except Exception as e:
        msg = ask_gemini(f"Explain politely that an error occurred while loading context: {e}, and Zen will use a default context.", [])
        zen_speak(msg)
        default_context = {"conversation_history": [], "user_preferences": {}}
        save_context(default_context)
        return default_context

def save_context(context):
    file_path = get_conversation_path(user)
    with context_lock:
        try:
            with open(file_path, "w") as f:
                json.dump(context, f, indent=4)
        except Exception as e:
            msg = ask_gemini(f"Explain politely that saving context failed with error: {e}.", [])
            zen_speak(msg)

def load_data_in_background():
    global reminders
    global context
    context = load_context()
    reminders = load_reminders()
    zen_data = load_and_decrypt()
    zen_data["last_used"] = datetime.now()
    encrypt_and_store(zen_data)

def check_and_install_requirements(requirements_file="requirements.txt"):
    print(f"[{os.path.basename(__file__)}] Checking and installing Python requirements...")
    if not os.path.exists(requirements_file):
        print(f"[{os.path.basename(__file__)}] Error: '{requirements_file}' not found in the current directory.")
        sys.exit(1)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        if "Requirement already satisfied" not in result.stdout or "Collecting" in result.stdout or "Installing" in result.stdout:
            print(f"[{os.path.basename(__file__)}] Requirements check complete. Dependencies are up-to-date or have been installed/updated.")
        else:
            print(f"[{os.path.basename(__file__)}] All requirements are already satisfied.")
    except subprocess.CalledProcessError as e:
        print(f"[{os.path.basename(__file__)}] Error installing/checking requirements:")
        print(f"[{os.path.basename(__file__)}] Command: {e.cmd}")
        print(f"[{os.path.basename(__file__)}] Stdout: {e.stdout}")
        print(f"[{os.path.basename(__file__)}] Stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"[{os.path.basename(__file__)}] An unexpected error occurred: {e}")
        sys.exit(1)

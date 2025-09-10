import os
import json
from cryptography.fernet import Fernet
from datetime import datetime

from interfaces.speech import zen_speak
from config import KEYS_DIR, CONVERSATIONS_DIR

KEY_FILE = os.path.join(KEYS_DIR, "zen_key.key")

def get_conversation_path(user):
    return os.path.join(CONVERSATIONS_DIR, f"{user}_conversation.json")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

if not os.path.exists(KEY_FILE):
    generate_key()

cipher = Fernet(load_key())

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

def save_secure_data(filename, data):
    encrypted_data = encrypt_data(json.dumps(data))
    with open(filename, "w") as file:
        file.write(encrypted_data)

def load_secure_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            encrypted_data = file.read()
        try:
            return json.loads(decrypt_data(encrypted_data))
        except Exception:
            zen_speak(f"Error: Could not decrypt or decode {filename}. File might be corrupted.")
            return {}
    return {}

def encrypt_and_store(data, filename="zen_data.json"):
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
    json_data = json.dumps(data).encode()
    encrypted_data = cipher.encrypt(json_data)
    file_path = os.path.join(CONVERSATIONS_DIR, filename)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def load_and_decrypt(filename="zen_data.json"):
    file_path = os.path.join(CONVERSATIONS_DIR, filename)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        decrypted_data = json.loads(decrypted_data)
    except Exception:
        zen_speak(f"Error: Could not decode JSON from {filename}. File might be corrupted.")
        return {}
    for key, value in decrypted_data.items():
        try:
            decrypted_data[key] = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return decrypted_data

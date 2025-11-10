#ZEN Secure Data Management Core (ZSDMC)

import re
import sqlite3
from cryptography.fernet import Fernet
import os

class ZSDMC:
    def __init__(self, key_file='zsdmc_key.key', db_file='zsdmc_vault.db'):
        self.key_file = key_file
        self.db_file = db_file
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
        self._init_db()

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS vault (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data_type TEXT,
                            encrypted_data TEXT)''')
        self.conn.commit()

    def classify_data(self, text):
        patterns = {
            "email": r"[\w\.-]+@[\w\.-]+",
            "password": r"(?=.*[A-Z])(?=.*\d).{8,}",
            "address": r"\d{1,3}\s[\w\s]+",
            "phone": r"\b\d{10}\b",
        }
        for dtype, pattern in patterns.items():
            if re.search(pattern, text):
                return dtype
        return None

    def encrypt_and_store(self, dtype, data):
        encrypted = self.cipher.encrypt(data.encode()).decode()
        self.conn.execute("INSERT INTO vault (data_type, encrypted_data) VALUES (?, ?)", (dtype, encrypted))
        self.conn.commit()

    def retrieve_data(self, dtype):
        cur = self.conn.cursor()
        cur.execute("SELECT encrypted_data FROM vault WHERE data_type=?", (dtype,))
        result = cur.fetchone()
        if result:
            return self.cipher.decrypt(result[0].encode()).decode()
        return "No stored data found for this type."

    def secure_process(self, text):
        dtype = self.classify_data(text)
        if dtype:
            self.encrypt_and_store(dtype, text)
            return f"Sensitive {dtype} data securely encrypted and stored locally."
        return None
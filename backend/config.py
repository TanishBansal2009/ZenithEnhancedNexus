import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

CONTEXT_DIR = os.path.join(TEMP_DIR, "context")
CONVERSATIONS_DIR = os.path.join(TEMP_DIR, "conversations")
KEYS_DIR = os.path.join(TEMP_DIR, "keys")
PROFILING_DIR = os.path.join(TEMP_DIR, "profiling")

for d in [TEMP_DIR, CONTEXT_DIR, CONVERSATIONS_DIR, KEYS_DIR, PROFILING_DIR]:
    os.makedirs(d, exist_ok=True)

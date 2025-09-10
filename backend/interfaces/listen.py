from termcolor import colored
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

from interfaces.speech import zen_speak
from core.users import user

try:
    model = Model(r"D:\Personal\Voice Assistants\Zen\Extra Files\vosk-model-en-us-0.22-lgraph")
    recognizer = KaldiRecognizer(model, 16000)
except Exception as e:
    model = None
    recognizer = None

def listen():
    if model is None or recognizer is None:
        zen_speak("Vosk model failed to load. Please type your response.")
        return input(colored(user, 'green') + " : ")

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16', channels=1) as stream:
            while True:
                data, overflowed = stream.read(8000)
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if result['text']:
                        return result['text']
    except OSError:
        zen_speak("Microphone error, please type your response.")
        return input(colored(user, 'green') + " : ")
    except Exception as e:
        print(f"Error in listen: {e}")
        zen_speak("An unexpected error occurred. Please type your response.")
        return input(colored(user, 'green') + " : ")
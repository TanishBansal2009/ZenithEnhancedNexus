import os
import requests

from interfaces.speech import zen_speak
from interfaces.gemini import ask_gemini
from core.context import context

api_key_weather = os.getenv("OPENWEATHER_API_KEY")
cities = os.getenv("CITIES_WEATHER", "").split(",")
weather_cache = {}

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city.strip(),
        "appid": api_key_weather, 
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            city = data["name"]
            country = data["sys"]["country"]

            return ask_gemini(
                f"As Zen, summarize: The weather in {city}, {country} is {weather}, "
                f"{temp}°C (feels like {feels_like}°C) with {humidity}% humidity.",
                context.get("conversation_history", [])
            )
        else:
            return ask_gemini(
                f"As Zen, explain politely: Sorry, I couldn't fetch weather for {city}.",
                context.get("conversation_history", [])
            )

    except Exception as e:
        return ask_gemini(
            f"As Zen, explain politely: Error while fetching weather: {str(e)}",
            context.get("conversation_history", [])
        )


def get_weather_for_cities(cities):
    return [get_weather(city) for city in cities if city]


def display_weather_updates(user_input):
    intent = ask_gemini(
        f"The user said: '{user_input}'. "
        "Are they asking about the weather? Answer YES or NO."
    , context.get("conversation_history", []))

    if intent.strip().lower().startswith("yes"):
        weather_reports = get_weather_for_cities(cities)

        if not weather_reports:
            zen_speak("No cities provided for weather updates.")
            return True

        for report in weather_reports:
            zen_speak(report)
        return True

    return False

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests
import os
from dotenv import load_dotenv  # To load environment variables from .env file
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher

# Load the .env file (if you're using it to store the API key)
load_dotenv()

class ActionGetWeather(Action):
    def name(self) -> str:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> list:
        # Get the location (e.g., Paris) from the user's input (use slot or message)
        location = tracker.get_slot("location")  # Assumes you have a slot named 'location'
        if not location:
            location = "Paris"  # Default location if none is provided

        # Get the API key from the environment variables
        api_key = os.getenv("    ") # Replace with your actual API key
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        url = f"{base_url}?q={location}&appid={api_key}"

        # Make the request to the weather API
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            # Parse the weather data
            main = weather_data["main"]
            weather_description = weather_data["weather"][0]["description"]
            temperature = main["temp"] - 273.15  # Convert from Kelvin to Celsius

            # Send the response back to the user
            dispatcher.utter_message(text=f"The current weather in {location} is {weather_description} with a temperature of {temperature:.2f}°C.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't get the weather data. Please try again later.")
        
        return []

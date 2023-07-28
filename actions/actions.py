from typing import Any, Text, Dict, List
import simplemma
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
import requests
import translators as ts


class ActionCheckWeather(Action):
    """Definition of class, which is responsible for retrieving weather information"""

    def name(self) -> Text:
        return "action_get_weather"

    def translate(self, text: str, to_lang: str = 'uk', from_lang: str = 'en'):
        return ts.translate_text(text, from_language=from_lang, to_language=to_lang).lower()

    def run(self, dispatcher, tracker, domain):

        # Processing location and date information from slots
        api_key = 'YOUR_API'
        loc = simplemma.lemmatize(str(tracker.get_slot('location')), lang='uk')
        loc_en = self.translate(loc, 'en', 'uk')  # To avoid mistakes caused uk language
        date = [simplemma.lemmatize(word, lang='uk') for word in str(tracker.get_slot('date')).strip().split()]

        # Define the default response in the event of an error
        response_def = "Вибачте, я не можу отримати погоду зараз. Перевірте правильність введених даних та спробуйте " \
                       "ще раз."

        # Trying to get current weather information
        try:
            current = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={loc_en}&appid={api_key}').json()
        except requests.exceptions.RequestException as e:
            # Обробка помилки
            dispatcher.utter_message(response_def)
            return [SlotSet('location', loc), SlotSet('date', date)]

        # Check the date and generate the appropriate response
        if ('сьогодні' in date or 'цей' in date or 'none' in date or 'зараз' in date):
            condition = current['weather'][0]['description']
            condition = self.translate(condition)
            temperature_c = round(current['main']['temp'] - 273.15, 1)
            response = f"{loc}, погода на сьогодні: {condition}, температура {round(temperature_c, 1)}"
        else:
            exclude = "minute,hourly"
            lon = current['coord']['lon']
            lat = current['coord']['lat']
            try:
                week_fc = requests.get(
                    f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}').json()
            except requests.exceptions.RequestException as e:
                # Обробка помилки
                dispatcher.utter_message(
                    "Вибачте, я не можу отримати погоду зараз. Спробуйте ще раз.")
                return [SlotSet('location', loc), SlotSet('date', date)]

            if ('наступний' in date or "завтра" in date):
                temperature_c = round(week_fc['daily'][1]['temp']['day'] - 273.15, 1)
                condition = week_fc['daily'][1]['weather'][0]['description']
                condition = self.translate(condition)
                response = f"{loc}, погода на завтра: {condition}, температура {temperature_c}"
            elif ('післязавтра' in date or "через" in date):
                temperature_c = round(week_fc['daily'][2]['temp']['day'] - 273.15, 1)
                condition = week_fc['daily'][2]['weather'][0]['description']
                condition = self.translate(condition)
                response = f"{loc}, погода на післязавтра: {condition}, температура {round(temperature_c, 1)}"

        try:
            dispatcher.utter_message(response)
        except UnboundLocalError:
            dispatcher.utter_message(response_def)

        return [SlotSet('location', loc), SlotSet('date', date)]


class ActionGoodbye(Action):
    """Definition of class, which is responsible for session termination """

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]  # Removing all data from slots

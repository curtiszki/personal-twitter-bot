# Module imports
import tweepy
import threading
from time import sleep
import owm_api

# The Twitter API OAuth keys should be in a credentials.py file.
from credentials import *

# Twitter OAuth via Tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class Tweeter:
    """Tweet and update based on OWM JSON data."""

    def __init__(self):
        self.message = None
        self.weather_values = None

    # Customized greeting based on the time before/after sunrise/sunset.
    def initial_greeting(self):
        weather_values = self.weather_values
        current_hour = int(weather_values.get('current_hour'))
        sunrise = int(weather_values.get('sunrise'))
        sunset = int(weather_values.get('sunset'))
        greeting = ''

        if type(sunset) != None and type(sunrise) != None and type(current_hour) != None:

            if current_hour <  sunrise - 2 or current_hour > sunset + 2:
                greeting = 'Right now in'
            elif current_hour  > sunrise + 2 and current_hour < sunset -2:
                greeting = 'Right now in'
            elif sunrise - 2 <= current_hour <= sunrise + 2:
                greeting = 'Good Morning'
            else:
                greeting = 'Good Night'
        else:
            greeting = 'Right now in'

        return greeting

    # Ensure the tweet is less than 140 characters, truncating if need be.
    def length_check(self, tweet):
        if len(tweet) > 140:
            tweet = tweet[:137] + '...'
        return tweet

    def init_values(self):
        self.weather_values = weather_values = owm_api.filter_json(owm_api.retrieve_data(owm_api.url_builder(CITY_ID, OWM_KEY)))
        unformatted_string = '{} {}, it is now {}, the temperature is {}\u00B0C with {}.'
        # values
        greeting = self.initial_greeting()
        city = weather_values.get('city')
        current_time = weather_values.get('current_time')
        temperature = weather_values.get('temperature')
        description = weather_values.get('description')
        formatted_string = unformatted_string.format(greeting, city, current_time, temperature, description)
        self.message = self.length_check(formatted_string)

    def tweet(self):
        threading.Timer(7200, self.tweet).start()
        self.init_values()
        print(self.message)
        try:
            api.update_status(self.message)
        except tweepy.TweepError as e:
            print(e.reason)

tweet = Tweeter()
tweet.tweet()

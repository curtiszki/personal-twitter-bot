# Module imports
import tweepy
from time import sleep
import owm_api

# The Twitter API OAuth keys should be in a credentials.py file.
from credentials import *

# Twitter OAuth via Tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

weather_values = owm_api.filter_json(owm_api.retrieve_data(owm_api.url_builder(CITY_ID, OWM_KEY)))

print(weather_values)
#for tweet in tweets:
#    api.update_status(tweet)
#    print(tweet)
#    sleep(20)
print("Check twitter")

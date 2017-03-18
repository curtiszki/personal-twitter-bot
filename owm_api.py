# Some functions to interact with the openweathermap api.

# Import the city id and api key.
from credentials import *
# data is UTC0 and needs to be converted to UTC+1
import datetime, urllib.request, json, pytz

# method to convert timestamp to UTC+1 Readable format.
def convert_time(timestamp):
    local_tz = pytz.timezone('America/Vancouver')
    target_tz = pytz.timezone('Europe/Paris')
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    local_dt = local_tz.localize(timestamp, is_dst=False)
    utc_dt = local_dt.astimezone(target_tz)
    utc_datetime =  suffixed_conversion('%I:%M%p, %B {D}', utc_dt)
    return utc_datetime

# proper suffixing for timestamp conversion.
def suffix_day(day):
    return 'th' if 11<=day<=13 else {1: 'st', 2:'nd', 3:'rd'}.get(day%10, 'th')

def suffixed_conversion(format, timestamp):
    return timestamp.strftime(format).replace('{D}', str(timestamp.day) + suffix_day(timestamp.day))
# construct the uri

def url_builder(city_id, api_key):
    baseurl = 'http://api.openweathermap.org/data/2.5/weather?id='
    units = 'metric'

    uri_complete = '{}{}&appid={}&units={}'.format(baseurl, city_id, api_key, units)
    return uri_complete

def retrieve_data(uri):
    with urllib.request.urlopen(uri) as uri:
        return json.loads(uri.read().decode('utf-8'))

def filter_json(json):

    sys = json.get('sys')
    sunrise = sys.get('sunrise')
    sunset = sys.get('sunset')

    current_time = convert_time(int(json.get('dt')))
    sunrise = convert_time(int(sunrise))
    sunset = convert_time(int(sunset))
    # for some reason there's a list nested...
    weather_desc = json.get('weather')[0].get('description')
    current_temp = json.get('main').get('temp')
    #The temp is X.XX so round it so it's a whole number
    current_temp = round(current_temp, 0)

    weather_values = dict(temperature=current_temp,
    description=weather_desc,
    current_time=current_time,
    sunrise=sunrise,
    sunset=sunset)

    return weather_values

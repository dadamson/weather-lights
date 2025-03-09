import datetime
import logging
import os
import pprint
import requests

log = logging.getLogger(__name__)

# Grab your API key here: http://openweathermap.org
# List of city ID city.list.json.gz can be downloaded here http://bulk.openweathermap.org/sample/
OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
OPENWEATHERMAP_CITY_ID = os.environ.get('OPENWEATHERMAP_CITY_ID')

OPENWEATHERMAP_FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'
OPENWEATHERMAP_CURRENT_URL = 'http://api.openweathermap.org/data/2.5/weather'


def get_forecast():
    log.debug(datetime.datetime.now())
    forecast = []
    payload = {
        'id': OPENWEATHERMAP_CITY_ID,
        'units': 'imperial',
        'appid': OPENWEATHERMAP_API_KEY
    }

    try:
        r = requests.get(url=OPENWEATHERMAP_CURRENT_URL, params=payload)
        snapshot = r.json()

        time = datetime.datetime.fromtimestamp(snapshot['dt'])
        temp = snapshot['main']['temp']
        if len(snapshot['weather']) > 1:
            log.debug('multiple weathers?')
            log.debug(snapshot['weather'])
        weather = snapshot['weather'][0]['main']
        weather_code = snapshot['weather'][0]['id']
        weather_desc = snapshot['weather'][0]['description']

        log.debug('{} = {}F, {} ({}={})'.format(time, temp, weather, weather_code, weather_desc))

        forecast.append(dict(time=time, temp=temp, weather=weather, code=weather_code, desc=weather_desc))

    except requests.exceptions.ConnectionError as ex:
        log.warning('OpenWeatherMap Connection Error:\n{}'.format(ex))

    try:
        r = requests.get(url=OPENWEATHERMAP_FORECAST_URL, params=payload)
        data = r.json()
        # log.debug(data)

        for snapshot in data['list']:
            time = datetime.datetime.fromtimestamp(snapshot['dt'])
            temp = snapshot['main']['temp']
            weather = snapshot['weather'][0]['main']
            weather_code = snapshot['weather'][0]['id']
            weather_desc = snapshot['weather'][0]['description']

            # log.debug('{} = {}F, {} ({}={})'.format(time, temp, weather, weather_code, weather_desc))

            forecast.append(dict(time=time, temp=temp, weather=weather, code=weather_code, desc=weather_desc))

    except requests.exceptions.ConnectionError as ex:
        log.warning('Connection Error:\n{}'.format(ex))

    return forecast
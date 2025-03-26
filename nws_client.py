import datetime
import logging
import pprint
import zoneinfo

import requests

import constants as cbx

log = logging.getLogger(__name__)

# https://www.weather.gov/documentation/services-web-api
# see https://weather-gov.github.io/api/gridpoints for information on how to select your gridpoint and station
# https://api.weather.gov/points/40.43,-79.91 -- get station / gridpoint URLs from lat,long

forecast_url = f"https://api.weather.gov/gridpoints/PBZ/81,66/forecast/hourly"
current_url = f"https://api.weather.gov/stations/KPIT/observations/latest"

my_zone = zoneinfo.ZoneInfo('America/New_York')


def get_forecast():
    request_time = datetime.datetime.now().astimezone(my_zone)
    log.debug(request_time)
    forecast = []

    try:
        raw_forecast_response = requests.get(forecast_url)
        hourly_forecasts = raw_forecast_response.json()['properties']['periods']

        raw_current_response = requests.get(current_url)
        current_dict = raw_current_response.json()['properties']

        # Current values. The order of variables needs to be the same as requested.
        # current_time = datetime.datetime.now()  #fromtimestamp(current.Time())
        current_temp = current_dict['temperature']['value']
        if current_temp is not None:
            current_time = datetime.datetime.fromisoformat(
                current_dict['timestamp']).astimezone(my_zone)

            isC = current_dict['temperature']['unitCode'] == 'wmoUnit:degC'
            if isC:
                current_temp = current_temp * 9/5 + 32

            present_descs = current_dict['presentWeather']
            if len(present_descs):
                print(present_descs)
                current_name = present_descs[0]['weather'].title()
                weather_descs = (str(v).title() for pw in present_descs[0]
                                 for k, v in (pw if type(pw) is dict else {'???': pw}).items() if v)
                current_desc = ' '.join(weather_descs)
            else:
                current_name = current_desc = current_dict.get('textDescription', 'Clear')
                print('???')
                pprint.pprint(current_dict)
                print('???')
            current_prec = (current_dict['precipitationLastHour'].get('value') or 0) * 0.0393701  # mm to inches

            current_weather = dict(
                time=current_time, temp=current_temp,
                precipitation=current_prec, precip_prob=100 if current_prec > 0.1 else 0,
                weather=current_name, desc=current_desc
            )
        else:
            current_weather = None

        for period in hourly_forecasts:
            h_time = datetime.datetime.fromisoformat(period['startTime']).astimezone(my_zone)
            if h_time > request_time + datetime.timedelta(hours=24):
                continue
            h_temp = period['temperature']

            isC = period['temperatureUnit'] == 'C'
            if isC:
                h_temp = h_temp * 9/5 + 32

            h_prob = period['probabilityOfPrecipitation']['value']

            expected_weathers = cbx.NO_PRECIP_WEATHER + cbx.PRECIP_WEATHER
            # print(period['shortForecast'])
            h_words = period['shortForecast'].split()
            h_matches = [w for w in h_words if any(ew.lower() in w.lower() for ew in expected_weathers)]
            if len(h_matches) == 0:
                h_matches = h_words
            h_name = h_matches[-1]
            h_desc = period['shortForecast']

            forecast.append(
                dict(time=h_time,
                     temp=h_temp,
                     precip_prob=h_prob,
                     weather=h_name,
                     desc=h_desc)
            )
        if current_weather:
            forecast.append(current_weather)

    except requests.exceptions.ConnectionError as ex:
        log.warning('weather.gov connection error:\n{}'.format(ex))

    return forecast


if __name__ == '__main__':
    request_time = datetime.datetime.now()
    print(request_time)
    main_forecast = get_forecast()
    for f in main_forecast:
        print(f)

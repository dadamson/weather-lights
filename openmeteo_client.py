import datetime
import logging
import pprint
import requests

import constants

log = logging.getLogger(__name__)

import openmeteo_requests
from retry_requests import retry

# Set up the Open-Meteo API client with cache and retry on error
retry_session = retry(retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40.4406,  # 40.4352911,
    "longitude": -79.9959,  #-79.9122215,
    "current": ["temperature_2m", "weather_code", "precipitation", "precipitation_probability"],
    "hourly": ["temperature_2m", "weather_code", "precipitation", "precipitation_probability"],
    "temperature_unit": "fahrenheit",
    "precipitation_unit": "inch",
    "timezone": "America/New_York",
    "forecast_days": 2
}


def get_forecast():
    log.debug(datetime.datetime.now())
    forecast = []

    try:

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Current values. The order of variables needs to be the same as requested.
        current = response.Current()
        current_time = datetime.datetime.now()  #fromtimestamp(current.Time())
        current_temp= current.Variables(0).Value()
        current_code = int(current.Variables(1).Value())
        current_prec = float(current.Variables(2).Value())
        current_prob = float(current.Variables(2).Value())

        current_name, current_desc = constants.wmo_code_4677[current_code]

        current_weather = dict(
            time=current_time, temp=current_temp, code=current_code,
            precipitation=current_prec, precip_prob=100 if current_prec > 0.1 else current_prob,
            weather=current_name, desc=current_desc
        )

        hourly = response.Hourly()
        hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
        temp_var = hourly.Variables(0)
        code_var = hourly.Variables(1)
        prec_var = hourly.Variables(2)
        prob_var = hourly.Variables(3)

        for j, h_time, in enumerate(hourly_time):
            h_code = int(code_var.Values(j))
            h_prec = prec_var.Values(j)
            h_prob = prob_var.Values(j)
            h_name, h_desc = constants.wmo_code_4677[h_code]
            forecast.append(
                dict(time=datetime.datetime.fromtimestamp(h_time),
                     temp=temp_var.Values(j),
                     code=h_code,
                     precipitation=h_prec,
                     precip_prob=h_prob,
                     weather=h_name,
                     desc=h_desc)
            )

        forecast.append(current_weather)
    except requests.exceptions.ConnectionError as ex:
        log.warning('OpenMeteo Connection Error:\n{}'.format(ex))

    return forecast


if __name__ == '__main__':
    main_forecast = get_forecast()
    for f in main_forecast:
        print(f)

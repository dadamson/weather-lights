#!/usr/bin/env python

import datetime
import json
import logging
import math
import os
import pprint
import random
import sys
import time
import zoneinfo

import nws_client as weather_client
import constants as cbx


log = logging.getLogger(__name__)

CURRENT_WEATHER = []

UNEXPECTED_LOG_PATH = 'unexpected_weather.json'
if os.path.exists(UNEXPECTED_LOG_PATH):
    with open(UNEXPECTED_LOG_PATH) as jfi:
        UNEXPECTED_WEATHER = json.load(jfi)
else:
    UNEXPECTED_WEATHER = {}


my_zone = zoneinfo.ZoneInfo('America/New_York')

try:
    import blinkt
except ImportError:
    log.error('blinkt is not installed (only DUMMY_BLINK available)')
    cbx.DUMMY_BLINK = True

if cbx.DUMMY_BLINK:
    class Blinker(object):
        def __init__(self):
            self.pixels = [(0, 0, 0)]*8
            self.pixel_char = '■'
            self.brightness = 1.0
            self.clear_on_exit = False

        def set_brightness(self, bright_frac):
            print(f'set_brightness({bright_frac})')
            self.brightness = bright_frac

        def set_pixel(self, i, r, g, b):
            self.pixels[i] = (int(r), int(g), int(b))

        def show(self):
            os.system('clear')
            data_string = '  '.join(','.join(f'{c}' for c in px) for px in self.pixels)
            pixel_string = '\n'.join(
                f'\033[38;2;{int(255 * math.sqrt(r/255))};{int(255 * math.sqrt(g/255))};{int(255 * math.sqrt(b/255))}m{self.pixel_char}\033[0m'
                for r, g, b in self.pixels)
            print(f'Pixel RGB\n{data_string}')
            print(pixel_string)
            if CURRENT_WEATHER:
                print('\n'.join(CURRENT_WEATHER))

        def set_clear_on_exit(self):
            print(f'set_clear_on_exit()')
            self.clear_on_exit = True

        def exit(self):
            if self.clear_on_exit:
                print('\x1b[1K')
            print('Exit!')

    blinkt = Blinker()


def show_graph(rgbs, reverse=cbx.REVERSE_LIGHTS):
    for pix, (r, g, b) in enumerate(rgbs):
        blinkt.set_pixel(7-pix if reverse else pix, r, g, b)
    blinkt.show()


def draw_weather(forecast, k, today=None):
    if not today:
        today = datetime.datetime.now(tz=my_zone)

    wakeup = today.replace(hour=6, minute=15)
    dinnertime = today.replace(hour=18, minute=30)
    bedtime = today.replace(hour=23, minute=00)
        
    if today >= bedtime or today <= wakeup:
        show_graph([[0, 0, 0]]*8)
        return
    
    if today >= dinnertime:
        today += datetime.timedelta(days=1)
        today = today.replace(hour=7, minute=0)

    early = today.replace(hour=6, minute=0)
    morning = today.replace(hour=7, minute=30)  # 6-8
    morning2 = today.replace(hour=9, minute=30)  # 8-10
    lunch = today.replace(hour=11, minute=30)  # 10-12
    lunch2 = today.replace(hour=12+1, minute=30)  # 12-2
    afternoon = today.replace(hour=12 + 3, minute=30)  # 2-4
    afternoon2 = today.replace(hour=12 + 5, minute=30)  # 4-6
    evening = today.replace(hour=12 + 7, minute=30)  # 6-8
    evening2 = today.replace(hour=12 + 9, minute=30)  # 8p

    holiday = is_holiday(today)

    pixels = [(0, 0, 0)] * 8
    black_pixels = [(0, 0, 0)] * 8
    
    morning_pix = [0]
    morning2_pix = [1]
    lunch_pix = [2]
    lunch2_pix = [3]
    afternoon_pix = [4]
    afternoon2_pix = [5]
    evening_pix = [6]
    evening2_pix = [7]
    
    blunk = False
    CURRENT_WEATHER.clear()

    # log.debug(today)
    for j, snap in enumerate(forecast):
        # log.debug(snap['time'])
        if snap['time'] < early:
            continue
            
        elif today <= morning and snap['time'] < morning:
            # log.debug('morning! {}'.format(snap))
            blink(pixels, morning_pix, snap, k, holiday)
            blunk = True

        elif today <= morning2 and snap['time'] < morning2:
            # log.debug('morning! {}'.format(snap))
            blink(pixels, morning2_pix, snap, k, holiday)
            blunk = True
            
        elif today <= lunch and snap['time'] < lunch:
            # log.debug('lunch! {}'.format(snap))
            blink(pixels, lunch_pix, snap, k, holiday)
            blunk = True

        elif today <= lunch2 and snap['time'] < lunch2:
            # log.debug('lunch! {}'.format(snap))
            blink(pixels, lunch2_pix, snap, k, holiday)
            blunk = True
            
        elif today <= afternoon and snap['time'] < afternoon:
            # log.debug('afternoon! {}'.format(snap))
            blink(pixels, afternoon_pix, snap, k, holiday)
            blunk = True

        elif today <= afternoon2 and snap['time'] < afternoon2:
            # log.debug('afternoon! {}'.format(snap))
            blink(pixels, afternoon2_pix, snap, k, holiday)
            blunk = True
            
        elif today <= evening and snap['time'] < evening:
            # log.debug('evening! {}'.format(snap))
            blink(pixels, evening_pix, snap, k, holiday)
            blunk = True

        elif today <= evening2 and snap['time'] < evening2:
            # log.debug('evening! {}'.format(snap))
            blink(pixels, evening2_pix, snap, k, holiday)
            blunk = True
            
        elif snap['time'] > evening2:
            continue

    if blunk and pixels != black_pixels:
        show_graph(pixels)
    else:
        time.sleep(60)


def is_holiday(today):
    holidays = cbx.HOLIDAYS

    for hh in holidays:
        (m1, d1), (m2, d2) = hh
        party_start = datetime.datetime(year=today.year, month=m1, day=d1, tzinfo=my_zone)
        party_end = datetime.datetime(year=today.year, month=m2, day=d2, tzinfo=my_zone)
        if party_start <= today.replace(hour=0, minute=0) <= party_end:
            return True
    return False


def blink(pixels, pix, snap, k, holiday=False):
    precip_amount = snap.get('precipitation', 0)
    precip_prob = snap.get('precip_prob', 0)
    if 'precip_prob' in snap:
        precip_extra = f' ({precip_prob}% chance of precipitation, ~{precip_amount:.1f} in)'
    else:
        precip_extra = ''
    weather_name = snap['weather']
    weather_desc = snap['desc']
    CURRENT_WEATHER.append(f"{snap['temp']:.0f}°F, {weather_name} {snap.get('code', '')} = {weather_desc}{precip_extra} "
                           f"@ {snap['time'].strftime('%m-%d-%H:%M')}")
    for x in pix:
        pixels[x] = (0, 0, 0)

    main_color = get_temp_color(snap['temp'])
    dim_color = [int(v * cbx.DIM_FACTOR) for v in main_color]
    half_dim_color = [int(v * (cbx.DIM_FACTOR + 1)/2) for v in main_color]      # TODO: see if this is nice

    avg_bright = sum(main_color)//3
    frost_color = normalize_rgb([(v+avg_bright)//2 for v in main_color], 128)   # TODO: see if this is nice

    if weather_name in cbx.NO_PRECIP_WEATHER or precip_prob <= 70:
        if 'Fog' in weather_name:
            main_color = frost_color  # dim_color
        if 'Mist' in weather_name or 'Haze' in weather_name:
            main_color = frost_color  # half_dim_color
        if 'Frost' in weather_name:
            main_color = frost_color

        for x in pix:
            pixels[x] = main_color

    # TODO: add another animation type or "dim" value for "precipitation probable but no forecast accumulation"
    # TODO: add a half-step flash-twinkle for Thunder
    elif any (w in weather_name for w in cbx.PRECIP_WEATHER) or precip_prob > 70:
        is_possible = precip_prob > 60 and precip_amount == 0  # is_light will also be true
        is_light = 'light' in weather_desc.lower() or ('precipitation' in snap and precip_amount < 0.1)
        is_heavy = 'heavy' in weather_desc.lower() or precip_amount > 0.3
        is_moderate = not is_light and not is_heavy
        
        if 'Snow' in weather_name:
            snow_white = min(255, 85 * cbx.NORMALIZE_COLORS // 128)
            blank = (snow_white, snow_white, snow_white)
            main_color = dim_color
        elif 'Thunderstorm' in weather_name and 'Slight Chance' not in weather_desc:
            blank = (0, 0, 0)
            if precip_prob > 30:
                main_color = dim_color
        elif is_possible:
            blank = half_dim_color
        elif is_light:
            blank = dim_color
        else:
            blank = main_color
            main_color = dim_color

        for j, x in enumerate(pix):
            if holiday and k % 32 < 8:
                light_string = cbx.PARTY_COLORS
                blank = light_string[(x-k)%len(light_string)]
                # print('!!! party blank', blank)

            # light precipitation
            if is_light and (x-k)%6 == 0:
                # print('*', x,  blank)
                pixels[x] = blank
            # moderate
            elif is_moderate and (x-k)%3 == 0:
                # print('**', x,  blank)
                pixels[x] = blank   
            # heavy
            elif is_heavy and (x-k)%2 == 0:
                # print('***', x,  blank)
                pixels[x] = blank
            else:
                # print('[]', x, blank)
                pixels[x] = main_color
        # print(pixels)
        
    else:  # weird weather
        print(f'WEIRD {snap}')
        blank = (0, 0, 0)
        for x in pix:
            if k % 2:
                pixels[x] = blank
            else:
                pixels[x] = main_color
        if weather_name not in UNEXPECTED_WEATHER:
            UNEXPECTED_WEATHER[weather_name] = snap
            with open(UNEXPECTED_LOG_PATH, 'w') as jfo:
                json.dump(UNEXPECTED_WEATHER, jfo)


def get_temp_color(temp, normalize=cbx.NORMALIZE_COLORS, blend=cbx.BLEND_COLORS):
    min_rgb = (255, 0, 0)
    max_temp = min(cbx.TEMPERATURE_COLORS.keys())
    min_temp = max_temp - 7

    max_rgb = (255, 0, 0)
    for max_temp, max_rgb in sorted(cbx.TEMPERATURE_COLORS.items()):
        if temp <= max_temp:
            break
        min_rgb = max_rgb
        min_temp = max_temp

    if max_temp == min_temp:
        max_temp += 7

    if normalize > 0:
        max_rgb = normalize_rgb(max_rgb, blend * 255 or normalize)
        min_rgb = normalize_rgb(min_rgb, blend * 255 or normalize)

    if blend:
        post_factor = max(0.0, min(1.0, (temp - min_temp) / (max_temp - min_temp)))
        pre_factor = 1.0 - post_factor
        # pre_factor = math.sqrt(1.0 - post_factor)
        # post_factor = 1.0 - pre_factor

        blend_rgb = tuple((post_factor * post_c + pre_factor * pre_c)
                          for post_c, pre_c in zip(max_rgb, min_rgb))
        blend_rgb = normalize_rgb(blend_rgb, normalize)

        return blend_rgb

    return max_rgb


def normalize_rgb(rgb, norm_target):
    magic = norm_target / sum(rgb)
    normed = [min(255, int(v * magic)) for v in rgb]
    return normed


def dummy_weather(today):
    temps = list(cbx.SAMPLE_TEMPS)
    times = [today.replace(hour=h, minute=0) for h in range(5, 23)]
    descriptions = ['light', 'moderate', 'heavy']
    warm_conditions = ['Haze', 'Tornado'] + ['Thunderstorm', 'Drizzle', 'Mist'] * 2 + ['Rain', 'Drizzle'] * 4 + ['Clear', 'Clouds'] * 6
    cold_conditions = ['Rain'] * 3 + ['Snow'] * 4 + ['Clear', 'Clouds'] * 6 + ['Fog', 'Mist']

    cold_temps = temps[:len(temps)//2]
    mid_temps = temps[len(temps)//3:2*len(temps)//3]
    warm_temps = temps[len(temps)//2:]

    weather_flavor = random.random()
    current_temps = warm_temps if weather_flavor < 0.33 else cold_temps if weather_flavor > 0.66 else mid_temps

    temp_now = None
    dummy_forecast = []
    current_conditions = []
    for time_ix, forecast_time in enumerate(times):
        warmer_time = forecast_time.hour < 11
        colder_time = forecast_time.hour > 16

        temp_choices = current_temps.copy()

        if temp_now is not None:
            if warmer_time:
                temp_choices = [t for t in current_temps if temp_now - 7 < t < temp_now + 21]
            elif colder_time:
                temp_choices = [t for t in current_temps if temp_now + 7 > t > temp_now - 21]
            temp_choices.extend([temp_now] * 4)

        temp_now = random.choice(temp_choices)

        if temp_now < 33:
            weather = random.choice(cold_conditions + current_conditions*8)
        elif temp_now > 55:
            weather = random.choice(warm_conditions + current_conditions*8)
        else:
            weather = random.choice(cold_conditions + warm_conditions + current_conditions*16)

        current_conditions.append(weather)

        if weather in cbx.PRECIP_WEATHER:
            desc = '{} {}'.format(weather, random.choice(descriptions)).title()
            precip_prob = random.randint(50, 100)
        else:
            desc = weather
            precip_prob = random.randint(0, 80)

        snapshot = dict(time=forecast_time, desc=desc, weather=weather, temp=temp_now, code=0, precip_prob=precip_prob)
        dummy_forecast.append(snapshot)
            
    return dummy_forecast


if __name__ == '__main__':
    blinkt.set_brightness(0.05)
    blinkt.set_clear_on_exit()

    do_test = len(sys.argv) > 1 and 'test' in sys.argv[1].lower()

    for _ in range(1 + 2 * do_test):  # + 7 * do_test):
        unique_colors = sorted(set(cbx.TEMPERATURE_COLORS.keys()))
        for i, t in enumerate(unique_colors):
            next_t = unique_colors[(i + 1) % len(unique_colors)]

            r1, g1, b1 = get_temp_color(t)
            r2, g2, b2 = get_temp_color(t + 3.5)

            r3, g3, b3 = get_temp_color(next_t)
            r4, g4, b4 = get_temp_color(next_t + 3.5)

            for i in range(0, 2):
                blinkt.set_pixel(i, r1, g1, b1)
            for i in range(2, 4):
                blinkt.set_pixel(i, r2, g2, b2)
            for i in range(4, 6):
                blinkt.set_pixel(i, r3, g3, b3)
            for i in range(6, 8):
                blinkt.set_pixel(i, r4, g4, b4)
            blinkt.show()
            print(i, t, t+3.5, next_t, next_t+3.5)
            time.sleep(0.25 + do_test * 2)

    if do_test:
        for i in range(10):
            today = datetime.datetime.now(tz=my_zone)
            today = today.replace(hour=7, minute=0)
            log.info(today)
            dummy_forecast = dummy_weather(today)
            for snap in dummy_forecast:
                print(snap)
            log.info('***')
            for j in range(32):
                draw_weather(dummy_forecast, j, today=today)
                time.sleep(cbx.TWINKLE_TIME)

    while True:
        try:
            print(cbx.TWINKLE_TIME)
            time.sleep(cbx.TWINKLE_TIME)
            forecast = weather_client.get_forecast()
            if len(forecast) == 0:
                print(f'{datetime.datetime.now().isoformat()}: No forecast data.')
                time.sleep(cbx.UPDATE_PERIOD)
            else:
                pprint.pprint(forecast[-1])
                for i in range(int(cbx.UPDATE_PERIOD / cbx.TWINKLE_TIME)):
                    # today = None
                    # today = datetime.datetime.now().replace(hour=6, minute=30)
                    time.sleep(cbx.TWINKLE_TIME)
                    draw_weather(forecast, i)  #, today=today)
                    time.sleep(cbx.TWINKLE_TIME)
        except Exception as ex:
            import traceback as tb
            tb.print_exc()
            print(ex)
            time.sleep(60)

import os

DUMMY_BLINK = int(os.environ.get('DUMMY_BLINK', 0))
REVERSE_LIGHTS = int(os.environ.get('REVERSE', 0))
BLEND_COLORS = int(os.environ.get('BLEND_COLORS', 0))
NORMALIZE_COLORS = int(os.environ.get('NORMALIZE', 128))
UPDATE_PERIOD = 60*int(os.environ.get('WEATHER_UPDATE_MIN', 15))
TWINKLE_TIME = float(os.environ.get('WEATHER_TWINKLE_TIME', 0.5))
DIM_FACTOR = 0.25

print(DUMMY_BLINK, REVERSE_LIGHTS, NORMALIZE_COLORS, UPDATE_PERIOD, TWINKLE_TIME)

PRECIP_WEATHER = ['Snow', 'Rain', 'Drizzle', 'Thunderstorm', 'Shower', 'Thunderstorms', 'Showers']
NO_PRECIP_WEATHER = ['Sunny', 'Clear', 'Clouds', 'Cloudy', 'Overcast', 'Fog', 'Mist', 'Haze', 'Frost']

PARTY_COLORS = [
    (128, 8, 0),
    (8, 128, 0),
    (96, 8, 32),
    (70, 8, 64),
    (88, 48, 0),
    (16, 8, 160),
    (108, 28, 0)
]
HOLIDAYS = [
    ((1, 1), (1, 2)),
    ((2, 13), (2, 15)),
    ((4, 7), (4, 9)),
    ((6, 24), (6, 28)),
    ((7, 3), (7, 5)),
    ((7, 27), (7, 29)),
    ((10, 27), (11, 2)),
    ((11, 24), (11, 30)),
    ((12, 12), (12, 31))
]
TEMPERATURE_COLORS = {
    -20: (128, 128, 128),  # Deadly White
    -9: (128, 128, 128),   # Deadly White
    -2: (255, 255, 192),   # Deadly White
    5:  (255, 255, 140),   # Paler Purple
    12: (255, 96, 140),    # Pale Pink
    19: (192, 8, 128),     # Pink-Purple
    26: (128, 0, 128),     # Blue-Purple
    33: (64, 0, 192),      # Purple-Blue  (64, 0, 224)
    40: (0, 16, 255),      # Very Blue
    47: (0, 64, 128),      # Blue-Teal   (0, 64, 192),
    54: (0, 128, 64),      # Green-Teal   (0, 192, 64),
    61: (0, 240, 32),      # Very Green
    68: (128, 224, 0),     # Yellow-Green
    75: (160, 128, 0),     # Very Yellow
    82: (255, 172, 0),      # Orange-Yellow
    89: (255, 128, 0),      # Orange
    96: (255, 32, 0),       # Orange-Red,
    103: (255, 0, 16),      # Very Red
    212: (255, 0, 64),      # Hot Magenta
}
SAMPLE_TEMPS = [-5, -5, 10, 10, 17, 17, 23, 23, 30, 30,
                37, 37, 44, 44, 51, 51, 58, 58, 65, 65,
                72, 72, 79, 79, 86, 86, 93, 93, 100, 100]
ZIP = '15217,us'

wmo_code_4677 = {
    0: ("Clear", "Cloud development not observed or not observable"),
    1: ("Clouds", "Clouds generally dissolving or becoming less developed"),
    2: ("Clouds", "State of sky on the whole unchanged"),
    3: ("Clouds", "Clouds generally forming or developing"),
    4: ("Haze", "Visibility reduced by smoke"),
    5: ("Haze", "Haze"),
    6: ("Haze", "Widespread dust in suspension in the air"),
    7: ("Haze", "Dust or sand raised by wind at or near the station"),
    8: ("Haze", "Well developed dust whirl(s) or sand whirl(s) seen"),
    9: ("Haze", "Duststorm or sandstorm within sight"),
    10: ("Mist", "Mist"),
    11: ("Fog", "Patches shallow fog or ice fog"),
    12: ("Fog", "More or less continuous"),
    13: ("Thunderstorm", "Lightning visible, no thunder heard"),
    14: ("Rain", "Precipitation within sight, not reaching the ground"),
    15: ("Rain", "Precipitation within sight, reaching the ground, but distant"),
    16: ("Rain", "Precipitation within sight, reaching the ground, near to the station"),
    17: ("Thunderstorm", "Thunderstorm, but no precipitation"),
    18: ("Thunderstorm", "Squalls at or within sight of the station"),
    19: ("Tornado", "Funnel cloud(s)"),
    20: ("Drizzle", "Drizzle (not freezing) or snow grains not falling as shower(s)"),
    21: ("Rain", "Rain (not freezing)"),
    22: ("Snow", "Snow"),
    23: ("Snow", "Rain and snow or ice pellets"),
    24: ("Drizzle", "Freezing drizzle or freezing rain"),
    25: ("Rain", "Shower(s) of rain"),
    26: ("Snow", "Shower(s) of snow, or of rain and snow"),
    27: ("Snow", "Shower(s) of hail, or of rain and hail"),
    28: ("Fog", "Fog or ice fog"),
    29: ("Thunderstorm", "Thunderstorm (with or without precipitation)"),
    30: ("Haze", "Slight or moderate duststorm or sandstorm - has decreased"),
    31: ("Haze", "Slight or moderate duststorm or sandstorm - no appreciable change"),
    32: ("Haze", "Slight or moderate duststorm or sandstorm - has begun or increased"),
    33: ("Haze", "Severe duststorm or sandstorm - has decreased"),
    34: ("Haze", "Severe duststorm or sandstorm - no appreciable change"),
    35: ("Haze", "Severe duststorm or sandstorm - has begun or increased"),
    36: ("Snow", "Slight or moderate blowing snow generally low"),
    37: ("Snow", "Heavy drifting snow"),
    38: ("Snow", "Slight or moderate blowing snow generally high"),
    39: ("Snow", "Heavy drifting snow"),
    40: ("Fog", "Fog or ice fog at a distance"),
    41: ("Fog", "Fog or ice fog in patches"),
    42: ("Fog", "Fog or ice fog, sky visible has become thinner"),
    43: ("Fog", "Fog or ice fog, sky invisible"),
    44: ("Fog", "Fog or ice fog, sky visible no appreciable change"),
    45: ("Fog", "Fog or ice fog, sky invisible"),
    46: ("Fog", "Fog or ice fog, sky visible has begun or become thicker"),
    47: ("Fog", "Fog or ice fog, sky invisible"),
    48: ("Fog", "Fog, depositing rime, sky visible"),
    49: ("Fog", "Fog, depositing rime, sky invisible"),
    50: ("Drizzle", "Drizzle, not freezing, intermittent slight"),
    51: ("Drizzle", "Drizzle, not freezing, continuous slight"),
    52: ("Drizzle", "Drizzle, not freezing, intermittent moderate"),
    53: ("Drizzle", "Drizzle, not freezing, continuous moderate"),
    54: ("Drizzle", "Drizzle, not freezing, intermittent heavy"),
    55: ("Drizzle", "Drizzle, not freezing, continuous heavy"),
    56: ("Drizzle", "Drizzle, freezing, slight"),
    57: ("Drizzle", "Drizzle, freezing, moderate or heavy"),
    58: ("Drizzle", "Drizzle and rain, slight"),
    59: ("Drizzle", "Drizzle and rain, moderate or heavy"),
    60: ("Rain", "Rain, not freezing, intermittent slight"),
    61: ("Rain", "Rain, not freezing, continuous slight"),
    62: ("Rain", "Rain, not freezing, intermittent moderate"),
    63: ("Rain", "Rain, not freezing, continuous moderate"),
    64: ("Rain", "Rain, not freezing, intermittent heavy"),
    65: ("Rain", "Rain, not freezing, continuous heavy"),
    66: ("Rain", "Rain, freezing, slight"),
    67: ("Rain", "Rain, freezing, moderate or heavy"),
    68: ("Rain", "Rain or drizzle and snow, slight"),
    69: ("Rain", "Rain or drizzle and snow, moderate or heavy"),
    70: ("Snow", "Intermittent fall of snowflakes slight"),
    71: ("Snow", "Continuous fall of snowflakes slight"),
    72: ("Snow", "Intermittent fall of snowflakes moderate"),
    73: ("Snow", "Continuous fall of snowflakes moderate"),
    74: ("Snow", "Intermittent fall of snowflakes heavy"),
    75: ("Snow", "Continuous fall of snowflakes heavy"),
    76: ("Snow", "Diamond dust"),
    77: ("Snow", "Snow grains"),
    78: ("Snow", "Isolated star-like snow crystals"),
    79: ("Snow", "Ice pellets"),
    80: ("Rain", "Rain shower(s), slight"),
    81: ("Rain", "Rain shower(s), moderate or heavy"),
    82: ("Rain", "Rain shower(s), violent"),
    83: ("Rain", "Shower(s) of rain and snow mixed, slight"),
    84: ("Rain", "Shower(s) of rain and snow mixed, moderate or heavy"),
    85: ("Snow", "Snow shower(s), slight"),
    86: ("Snow", "Snow shower(s), moderate or heavy"),
    87: ("Snow", "Shower(s) of snow pellets or small hail, slight"),
    88: ("Snow", "Shower(s) of snow pellets or small hail, moderate or heavy"),
    89: ("Snow", "Shower(s) of hail, not associated with thunder, slight"),
    90: ("Snow", "Shower(s) of hail, not associated with thunder, moderate or heavy"),
    91: ("Rain", "Slight rain, thunderstorm during preceding hour"),
    92: ("Rain", "Moderate or heavy rain, thunderstorm during preceding hour"),
    93: ("Snow", "Slight snow, or rain and snow mixed or hail at time of observation"),
    94: ("Snow", "Moderate or heavy snow, or rain and snow mixed or hail at time of observation"),
    95: ("Thunderstorm", "Thunderstorm, slight or moderate, without hail but with rain and/or snow at time of observation"),
    96: ("Thunderstorm", "Thunderstorm, slight or moderate, with hail at time of observation"),
    97: ("Thunderstorm", "Thunderstorm, heavy, without hail but with rain and/or snow at time of observation"),
    98: ("Thunderstorm", "Thunderstorm combined with duststorm or sandstorm at time of observation"),
    99: ("Thunderstorm", "Thunderstorm, heavy, with hail at time of observation"),
}
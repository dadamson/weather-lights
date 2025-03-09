Display the current and forecast weather conditions on a [Pimoroni Blinkt!](https://shop.pimoroni.com/products/blinkt) LED strip for a Raspberry Pi Zero. 
If the `blinkt` library is not installed, the "DUMMY_BLINK" mode will display colored square characters in the terminal instead, simulating the LED output.

Run `python cloudberry_weather_lights.py` 

There are a few constants in [constants.py](constants.py) that you can set to control the behavior. Some of them can be set with environment variables:

```python
# output to terminal instead of blinkt
DUMMY_BLINK = int(os.environ.get('DUMMY_BLINK', 0))

# which way is "up"? Time and precipitation should progress from top to bottom.
REVERSE_LIGHTS = int(os.environ.get('REVERSE', 0))

# interpolate the color values between TEMPERATURE_COLORS values
BLEND_COLORS = int(os.environ.get('BLEND_COLORS', 0))

# normalize a color tuple to a given "total brightness" (eg, sum of R, G, B values)
NORMALIZE_COLORS = int(os.environ.get('NORMALIZE', 128))

#minutes between weather API calls
UPDATE_PERIOD = 60*int(os.environ.get('WEATHER_UPDATE_MIN', 15))

# seconds between blinks
TWINKLE_TIME = float(os.environ.get('WEATHER_TWINKLE_TIME', 0.5))
```

And also a few big maps of constants for special days, temperature colors, and weather code lookup.

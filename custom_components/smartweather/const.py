"""Constants in smartweather component."""
import logging

from pysmartweatherio import (
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
    FORECAST_TYPES,
)

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN

DOMAIN = "smartweather"

ATTR_SMARTWEATHER_STATION_NAME = "station_name"
ATTR_SMARTWEATHER_STATION_ID = "station_id"
ATTR_TEMP_HIGH_TODAY = "temp_high_today"
ATTR_TEMP_LOW_TODAY = "temp_low_today"
ATTR_UPDATED = "updated"
ATTR_BRAND = "Brand"
ATTR_CURRENT_ICON = "current_icon"
ATTR_FCST_UV = "uv"
CONF_STATION_ID = "station_id"
CONF_WIND_UNIT = "wind_unit"
CONF_ADD_SENSORS = "add_sensors"
CONF_FORECAST_TYPE = "forecast_type"
CONF_FORECAST_INTERVAL = "forecast_interval"

SMARTWEATHER_PLATFORMS = [
    "binary_sensor",
    "sensor",
    "weather",
]

WIND_UNITS = [
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
]

DEFAULT_BRAND = "WeatherFlow"
DEFAULT_ATTRIBUTION = "Powered by a WeatherFlow Smart Weather Station"
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_FORECAST_INTERVAL = 5

DEVICE_TYPE_WEATHER = "weather"

LOGGER = logging.getLogger(__package__)

CONDITION_CLASSES = {
    "clear-night": ["clear-night"],
    "cloudy": ["cloudy"],
    "exceptional": ["cloudy"],
    "fog": ["foggy"],
    "hail": ["hail"],
    "lightning": ["thunderstorm"],
    "lightning-rainy": ["possibly-thunderstorm-day", "possibly-thunderstorm-night"],
    "partlycloudy": [
        "partly-cloudy-day",
        "partly-cloudy-night",
    ],
    "pouring": ["rainy"],
    "rainy": [
        "rainy",
        "possibly-rainy-day",
        "possibly-rainy-night",
    ],
    "snowy": ["snow", "possibly-snow-day", "possibly-snow-night"],
    "snowy-rainy": ["sleet", "possibly-sleet-day", "possibly-sleet-night"],
    "sunny": ["clear-day"],
    "windy": ["windy"],
    "windy-variant": ["windy"],
}

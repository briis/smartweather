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
    "clear-night": ["cc-clear-night", "clear-night"],
    "cloudy": ["cc-cloudy", "cloudy"],
    "exceptional": [],
    "fog": ["cc-fog", "fog"],
    "hail": ["cc-hail", "hail"],
    "lightning": ["cc-thunderstorm", "thunderstorm"],
    "lightning-rainy": [200, 201, 202],
    "partlycloudy": [
        "cc-partly-cloudy-day",
        "cc-partly-cloudy-night",
        "partly-cloudy-day",
        "partly-cloudy-night",
        "possibly-rainy-day",
        "possibly-rainy-night",
        "cc-possibly-rainy-day",
        "cc-possibly-rainy-night",
    ],
    "pouring": ["cc-thunderstorm", "thunderstorm"],
    "rainy": ["rainy", "chance-rain", "cc-rainy", "cc-chance-rain",],
    "snowy": [600, 601, 602, 621, 622, 623],
    "snowy-rainy": [610, 611, 612],
    "sunny": ["cc-clear-day", "clear-day"],
    "windy": [],
    "windy-variant": [],
}

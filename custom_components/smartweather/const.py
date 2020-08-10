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
)

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN

DOMAIN = "smartweather"

ATTR_STATION_NAME = "station_name"
ATTR_UPDATED = "updated"
CONF_STATION_ID = "station_id"
CONF_WIND_UNIT = "wind_unit"
CONF_ADD_SENSORS = "add_sensors"

ENTITY_ID_SENSOR_FORMAT = SENSOR_DOMAIN + "." + "{}_{}"
ENTITY_ID_BINARY_SENSOR_FORMAT = BINARY_SENSOR_DOMAIN + "." + "{}_{}"
ENTITY_UNIQUE_ID = DOMAIN + "_{}_{}"

SMARTWEATHER_PLATFORMS = [
    "binary_sensor",
    "sensor",
]

WIND_UNITS = [
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
]

DEFAULT_ATTRIBUTION = "Weather data powered by a SmartWeather Weather Station"
DEFAULT_SCAN_INTERVAL = 60

LOGGER = logging.getLogger(__package__)

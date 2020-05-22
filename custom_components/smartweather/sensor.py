"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create sensors for each type.

    For a full description, go here: https://github.com/briis/smartweather

    Author: Bjarne Riis
"""
import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_ID,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    LENGTH_METERS,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    UV_INDEX,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import slugify
from .const import (
    DOMAIN,
    DEFAULT_ATTRIBUTION,
    CONF_STATION_ID,
    ENTITY_ID_SENSOR_FORMAT,
    ENTITY_UNIQUE_ID,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
)

_LOGGER = logging.getLogger(__name__)

ATTR_LIGHTNING_DETECTED = "last_detected"
ATTR_LIGHTNING_DISTANCE = "lightning_distance"
ATTR_LIGHTNING_LAST_3HOUR = "lightning_last_3hr"
ATTR_LAST_UPDATE = "last_update"
ATTR_STATION_LOCATION = "station_location"
ATTR_STATION_POSITION = "station_position"

# Sensor types are defined like: Name, Unit Type, icon, device class
SENSOR_TYPES = {
    "air_temperature": [
        "Temperature",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "feels_like": [
        "Feels Like",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "heat_index": [
        "Heat Index",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "wind_chill": [
        "Wind Chill",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "dew_point": [
        "Dewpoint",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
    ],
    "wind_avg": ["Wind Speed", UNIT_TYPE_WIND, "mdi:weather-windy", None],
    "wind_bearing": ["Wind Bearing", "°", "mdi:compass-outline", None],
    "wind_direction": ["Wind Direction", None, "mdi:compass-outline", None],
    "wind_gust": ["Wind Gust", UNIT_TYPE_WIND, "mdi:weather-windy", None],
    "precip_accum_local_day": ["Rain today", UNIT_TYPE_RAIN, "mdi:weather-rainy", None],
    "precip_rate": ["Rain rate", UNIT_TYPE_RAIN, "mdi:weather-pouring", None],
    "precip_accum_last_1hr": [
        "Rain last hour",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
    ],
    "precip_accum_local_yesterday": [
        "Rain yesterday",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
    ],
    "relative_humidity": ["Humidity", "%", "mdi:water-percent", DEVICE_CLASS_HUMIDITY],
    "station_pressure": [
        "Pressure",
        UNIT_TYPE_PRESSURE,
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
    ],
    "uv": ["UV", "UV", "mdi:weather-sunny", None],
    "solar_radiation": ["Solar Radiation", "W/m2", "mdi:solar-power", None],
    "brightness": ["Brightness", "Lx", "mdi:brightness-5", DEVICE_CLASS_ILLUMINANCE,],
    "lightning_strike_count": ["Lightning Count", None, "mdi:weather-lightning", None],
    "precip_minutes_local_day": ["Rain minutes today", "min", "mdi:timer", None],
    "precip_minutes_local_yesterday": [
        "Rain minutes yesterday",
        "min",
        "mdi:timer",
        None,
    ],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the Meteobridge sensor platform."""
    coordinator = hass.data[DOMAIN][entry.data[CONF_ID]]["coordinator"]
    if not coordinator.data:
        return

    smartweather = hass.data[DOMAIN][entry.data[CONF_ID]]["smw"]
    if not smartweather:
        return
    units = await smartweather.get_units()

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            SmartWeatherSensor(coordinator, sensor, units, entry.data[CONF_STATION_ID])
        )
        _LOGGER.debug(f"SENSOR ADDED: {sensor}")
    async_add_entities(sensors, True)

    return True


class SmartWeatherSensor(Entity):
    """ Implementation of a SmartWeather Weatherflow Sensor. """

    def __init__(self, coordinator, sensor, units, station_id):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._units = units
        self._sensor = sensor
        self._state = None
        self._name = SENSOR_TYPES[self._sensor][0]
        self.entity_id = ENTITY_ID_SENSOR_FORMAT.format(
            station_id, slugify(self._name).replace(" ", "_")
        )
        self._unique_id = ENTITY_UNIQUE_ID.format(station_id, self._sensor)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        value = getattr(self.coordinator.data[0], self._sensor, None)
        if not isinstance(value, str):
            return round(value, 1)

        return value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if SENSOR_TYPES[self._sensor][1] in self._units:
            return self._units[SENSOR_TYPES[self._sensor][1]]

        return SENSOR_TYPES[self._sensor][1]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return SENSOR_TYPES[self._sensor][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][3]

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr[ATTR_ATTRIBUTION] = DEFAULT_ATTRIBUTION

        return attr

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

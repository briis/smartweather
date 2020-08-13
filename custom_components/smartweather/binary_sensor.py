"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create a few binary sensors.

    For a full description, go here: https://github.com/briis/smartweather

    Author: Bjarne Riis
"""
import logging
from datetime import timedelta

try:
    from homeassistant.components.binary_sensor import (
        BinarySensorEntity as BinarySensorDevice,
    )
except ImportError:
    # Prior to HA v0.110
    from homeassistant.components.binary_sensor import BinarySensorDevice

from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_ID,
)
from homeassistant.components.binary_sensor import ENTITY_ID_FORMAT
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.entity import Entity, generate_entity_id
from .const import (
    DOMAIN,
    DEFAULT_ATTRIBUTION,
    ATTR_UPDATED,
    CONF_STATION_ID,
    CONF_ADD_SENSORS,
)

from .entity import SmartWeatherEntity

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "raining": ["Raining", None, "mdi:water", "mdi:water-off"],
    "freezing": ["Freezing", None, "mdi:fridge", "mdi:fridge-outline"],
    "lightning": ["Lightning", None, "mdi:weather-lightning", "mdi:flash-off"],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Add binary sensors for SmartWeather"""

    # Exit if user did deselect sensors and alerts on config
    if not entry.data[CONF_ADD_SENSORS]:
        return

    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    station_info = hass.data[DOMAIN][entry.entry_id]["station"]
    if not station_info:
        return

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            SmartWeatherBinarySensor(
                coordinator, entry.data, sensor, station_info, fcst_coordinator
            )
        )
        _LOGGER.debug(f"BINARY SENSOR ADDED: {sensor}")

    async_add_entities(sensors, True)

    return True


class SmartWeatherBinarySensor(SmartWeatherEntity, BinarySensorDevice):
    """ Implementation of a SmartWeather Weatherflow Binary Sensor. """

    def __init__(self, coordinator, entries, sensor, station_info, fcst_coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, entries, sensor, station_info, fcst_coordinator)
        self._sensor = sensor
        self._device_class = SENSOR_TYPES[self._sensor][1]
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][0]}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return getattr(self.coordinator.data[0], self._sensor) is True

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return (
            SENSOR_TYPES[self._sensor][2]
            if getattr(self.coordinator.data[0], self._sensor)
            else SENSOR_TYPES[self._sensor][3]
        )

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][1]

    # @property
    # def device_state_attributes(self):
    #     """Return the state attributes of the device."""
    #     return {
    #         ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
    #         # ATTR_STATION_NAME: getattr(self.coordinator.data[0], "station_name", None),
    #         # ATTR_STATION_NAME: self._station,
    #         # ATTR_UPDATED: getattr(self.coordinator.data[0], "timestamp", None),
    #     }

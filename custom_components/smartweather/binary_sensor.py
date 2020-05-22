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
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import slugify
from .const import (
    DOMAIN,
    DEFAULT_ATTRIBUTION,
    ATTR_STATION_NAME,
    ATTR_UPDATED,
    ENTITY_ID_BINARY_SENSOR_FORMAT,
    ENTITY_UNIQUE_ID,
    CONF_STATION_ID,
)

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

    coordinator = hass.data[DOMAIN][entry.data[CONF_ID]]["coordinator"]
    if not coordinator.data:
        return

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            SmartWeatherBinarySensor(coordinator, sensor, entry.data[CONF_ID])
        )
        _LOGGER.debug(f"BINARY SENSOR ADDED: {sensor}")

    async_add_entities(sensors, True)

    return True


class SmartWeatherBinarySensor(BinarySensorDevice):
    """ Implementation of a SmartWeather Weatherflow Current Sensor. """

    def __init__(self, coordinator, sensor, instance):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor = sensor
        self._device_class = SENSOR_TYPES[self._sensor][1]
        self._name = SENSOR_TYPES[self._sensor][0]
        self._station = instance
        self.entity_id = ENTITY_ID_BINARY_SENSOR_FORMAT.format(
            slugify(instance), slugify(self._name).replace(" ", "_")
        )
        self._unique_id = ENTITY_UNIQUE_ID.format(slugify(instance), self._sensor)

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

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

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
            # ATTR_STATION_NAME: getattr(self.coordinator.data[0], "station_name", None),
            ATTR_STATION_NAME: self._station,
            ATTR_UPDATED: getattr(self.coordinator.data[0], "timestamp", None),
        }

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

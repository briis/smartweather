"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create sensors for each type.

    For a full description, go here: https://github.com/briis/hass-SmartWeather

    Author: Bjarne Riis

"""
import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from . import DATA_SMARTWEATHER, CONF_NAME, ATTRIBUTION
from homeassistant.components.sensor import ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_MONITORED_CONDITIONS, TEMP_CELSIUS, LENGTH_METERS,
    UNIT_UV_INDEX, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_PRESSURE, DEVICE_CLASS_ILLUMINANCE)
from homeassistant.helpers.entity import Entity, generate_entity_id

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['smartweather']

ATTR_LAST_UPDATE = 'last_update'
ATTR_STATION_LOCATION = 'station_location'
ATTR_STATION_POSITION = 'station_position'
ATTR_LIGHTNING_DETECTED = 'last_detected'
ATTR_LIGHTNING_DISTANCE = 'lightning_distance'
ATTR_LIGHTNING_LAST_3HOUR = 'lightning_last_3hr'

# Sensor types are defined like: Name, Metric unit, icon, device class, Imperial unit
SENSOR_TYPES = {
    'temperature': ['Temperature', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'feels_like_temperature': ['Feels Like', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'heat_index': ['Heat Index', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'wind_chill': ['Wind Chill', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'dewpoint': ['Dewpoint', TEMP_CELSIUS, 'mdi:thermometer', DEVICE_CLASS_TEMPERATURE, None],
    'wind_speed': ['Wind Speed', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'wind_bearing': ['Wind Bearing', '°', 'mdi:compass-outline', None, None],
    'wind_direction': ['Wind Direction', None, 'mdi:compass-outline', None, None],
    'wind_gust': ['Wind Gust', 'm/s', 'mdi:weather-windy', None, 'mph'],
    'precipitation': ['Rain today', 'mm', 'mdi:weather-rainy', None, 'in'],
    'precipitation_rate': ['Rain rate', 'mm/h', 'mdi:weather-pouring', None, 'in/h'],
    'precipitation_last_1hr': ['Rain last hour', 'mm', 'mdi:weather-rainy', None, 'in'],
    'precipitation_last_24hr': ['Rain last 24hr', 'mm', 'mdi:weather-rainy', None, 'in'],
    'precipitation_yesterday': ['Rain yesterday', 'mm', 'mdi:weather-rainy', None, 'in'],
    'humidity': ['Humidity', '%', 'mdi:water-percent', DEVICE_CLASS_HUMIDITY, None],
    'pressure': ['Pressure', 'hPa', 'mdi:gauge', DEVICE_CLASS_PRESSURE, 'inHg'],
    'uv': ['UV', UNIT_UV_INDEX,'mdi:weather-sunny', None, None],
    'solar_radiation': ['Solar Radiation', 'W/m2', 'mdi:solar-power', None, None],
    'illuminance': ['Illuminance', 'Lx', 'mdi:brightness-5', DEVICE_CLASS_ILLUMINANCE, None],
    'lightning': ['Lightning', None, 'mdi:flash', None, None]
}


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SENSOR_TYPES)):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)])
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SmartWeather sensor platform."""
    if hass.config.units.is_metric:
        unit_system = 'metric'
    else:
        unit_system = 'imperial'

    data = hass.data[DATA_SMARTWEATHER]
    name = hass.data[CONF_NAME]

    if data.data.timestamp is None:
        return

    sensors = []
    for variable in config[CONF_MONITORED_CONDITIONS]:
        sensors.append(SmartWeatherCurrentSensor(hass, data, variable, name, unit_system))
        _LOGGER.debug("Sensor added: " + variable)

    add_entities(sensors, True)

class SmartWeatherCurrentSensor(Entity):
    """ Implementation of a SmartWeather Weatherflow Current Sensor """

    def __init__(self, hass, data, condition, name, unit_system):
        """Initialize the sensor."""
        self._condition = condition
        self._unit_system = unit_system
        self.data = data
        self._name = SENSOR_TYPES[self._condition][0]
        self.entity_id = generate_entity_id(ENTITY_ID_FORMAT, '{} {}'.format(name, SENSOR_TYPES[self._condition][0]), hass=hass)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if hasattr(self.data.data, self._condition):
            variable = getattr(self.data.data, self._condition)
            if not (variable is None):
                return variable
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        if self._unit_system == 'imperial' and not (SENSOR_TYPES[self._condition][4] is None):
            return SENSOR_TYPES[self._condition][4]
        else:
            return SENSOR_TYPES[self._condition][1]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return SENSOR_TYPES[self._condition][2]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._condition][3]

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr[ATTR_ATTRIBUTION] = ATTRIBUTION
        attr[ATTR_LAST_UPDATE] = self.data.data.timestamp
        attr[ATTR_STATION_LOCATION] = self.data.data.station_location
        attr[ATTR_STATION_POSITION] = 'Lat: '+str(self.data.data.latitude)+', Lon: '+str(self.data.data.longitude)

        if self._name.lower() == 'lightning':
            if self._unit_system == 'imperial':
                distance_unit = 'mi'
            else:
                distance_unit = 'km'
            attr[ATTR_LIGHTNING_DETECTED] = self.data.data.lightning_time
            attr[ATTR_LIGHTNING_LAST_3HOUR] = self.data.data.lightning_count_3hour
            attr[ATTR_LIGHTNING_DISTANCE] = str(self.data.data.lightning_distance) + ' ' + distance_unit

        return attr

    def update(self):
        """Update current conditions."""
        self.data.update()

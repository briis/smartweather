"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create sensors for each type.

    For a full description, go here: https://github.com/briis/smartweather

    Author: Bjarne Riis
"""
import logging
from typing import Dict

# from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from pysmartweatherio import (
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
)
from .const import (
    ATTR_DEVICE_TYPE,
    ATTR_SMARTWEATHER_STATION_ID,
    DEFAULT_ATTRIBUTION,
    DOMAIN,
    CONF_ADD_SENSORS,
)
from .entity import SmartWeatherEntity

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = 0
SENSOR_UNIT = 1
SENSOR_ICON = 2
SENSOR_DEVICE_CLASS = 3
SENSOR_STATE_CLASS = 4
SENSOR_IGNORE_ZERO = 5

STATE_CLASS_MEASUREMENT = "measurement"
STATE_CLASS_TOTAL_INCREASING = "total_increasing"

# Sensor types are defined like: Name, Unit Type, icon, device class, state class, Ignore on 0 Value
SENSOR_TYPES = {
    "air_temperature": [
        "Temperature",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "air_density": [
        "Air Density",
        "kg/m3",
        "mdi:weight-kilogram",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "feels_like": [
        "Feels Like",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "heat_index": [
        "Heat Index",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "wind_chill": [
        "Wind Chill",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        None,
        False,
    ],
    "dew_point": [
        "Dewpoint",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "wind_avg": [
        "Wind Speed",
        UNIT_TYPE_WIND,
        "mdi:weather-windy",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "wind_bearing": [
        "Wind Bearing",
        "°",
        "mdi:compass-outline",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "wind_direction": [
        "Wind Direction",
        None,
        "mdi:compass-outline",
        None,
        None,
        False,
    ],
    "wind_gust": [
        "Wind Gust",
        UNIT_TYPE_WIND,
        "mdi:weather-windy",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "precip_accum_local_day": [
        "Rain today",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "precip_rate": [
        "Rain rate",
        UNIT_TYPE_RAIN,
        "mdi:weather-pouring",
        None,
        None,
        False,
    ],
    "precip_accum_last_1hr": [
        "Rain last hour",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        None,
        False,
    ],
    "precip_accum_local_yesterday": [
        "Rain yesterday",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        None,
        False,
    ],
    "pressure_trend": [
        "Pressure Trend",
        None,
        "mdi:trending-up",
        None,
        None,
        False,
    ],
    "relative_humidity": [
        "Humidity",
        "%",
        "mdi:water-percent",
        DEVICE_CLASS_HUMIDITY,
        STATE_CLASS_MEASUREMENT,
        True,
    ],
    "station_pressure": [
        "Pressure",
        UNIT_TYPE_PRESSURE,
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
        STATE_CLASS_MEASUREMENT,
        True,
    ],
    "sea_level_pressure": [
        "Sea Level Pressure",
        UNIT_TYPE_PRESSURE,
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
        STATE_CLASS_MEASUREMENT,
        True,
    ],
    "uv": [
        "UV",
        "UV",
        "mdi:weather-sunny",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "solar_radiation": [
        "Solar Radiation",
        "W/m2",
        "mdi:solar-power",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "brightness": [
        "Brightness",
        "Lx",
        "mdi:brightness-5",
        DEVICE_CLASS_ILLUMINANCE,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "lightning_strike_count": [
        "Lightning Count",
        None,
        "mdi:weather-lightning",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "lightning_strike_last_distance": [
        "Lightning Distance",
        UNIT_TYPE_DISTANCE,
        "mdi:weather-lightning",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "lightning_strike_last_time": [
        "Lightning Time",
        "",
        "mdi:clock-outline",
        "timestamp",
        None,
        False,
    ],
    "lightning_strike_count_last_1hr": [
        "Lightning Last 1Hrs",
        "",
        "mdi:history",
        None,
        None,
        False,
    ],
    "lightning_strike_count_last_3hr": [
        "Lightning Last 3Hrs",
        "",
        "mdi:history",
        None,
        None,
        False,
    ],
    "precip_minutes_local_day": [
        "Rain minutes today",
        "min",
        "mdi:timer-outline",
        None,
        STATE_CLASS_MEASUREMENT,
        False,
    ],
    "precip_minutes_local_yesterday": [
        "Rain minutes yesterday",
        "min",
        "mdi:timer-outline",
        None,
        None,
        False,
    ],
    "station_information": [
        "Station information",
        "",
        "mdi:windsock",
        None,
        None,
        False,
    ],
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:

    # Exit if user did deselect sensors and alerts on config
    if not entry.data[CONF_ADD_SENSORS]:
        return False

    # Set up the Meteobridge sensor platform.
    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return False

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return False

    device_coordinator = hass.data[DOMAIN][entry.entry_id]["device_coordinator"]
    if not device_coordinator.data:
        return False

    smartweather = hass.data[DOMAIN][entry.entry_id]["smw"]
    if not smartweather:
        return False
    units = await smartweather.get_units()

    station_info = hass.data[DOMAIN][entry.entry_id]["station"]
    if not station_info:
        return False

    unit_system = "metric" if hass.config.units.is_metric else "imperial"

    for batsensor in device_coordinator.data:
        # Append Battery Devices to SENSOR_TYPES
        key = f"battery_{batsensor.device_type_desc}_{batsensor.device_id}"
        SENSOR_TYPES.setdefault(key, [])
        SENSOR_TYPES[key] = [
            f"Battery {batsensor.device_name}",
            "V",
            "mdi:battery",
            DEVICE_CLASS_VOLTAGE,
            STATE_CLASS_MEASUREMENT,
            False,
        ]

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(
            SmartWeatherSensor(
                coordinator,
                entry.data,
                sensor,
                units,
                station_info,
                fcst_coordinator,
                device_coordinator,
                unit_system,
            )
        )
        _LOGGER.debug("SENSOR ADDED: %s", sensor)

    async_add_entities(sensors, True)
    return True


class SmartWeatherSensor(SmartWeatherEntity, SensorEntity):
    """ Implementation of a SmartWeather Weatherflow Sensor. """

    def __init__(
        self,
        coordinator,
        entries,
        sensor,
        units,
        station_info,
        fcst_coordinator,
        device_coordinator,
        unit_system,
    ):
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            entries,
            sensor,
            station_info,
            fcst_coordinator,
            device_coordinator,
        )
        self._units = units
        self._unit_system = unit_system
        self._sensor = sensor
        self._state = None
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][SENSOR_NAME]}"
        self._station_info = station_info

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""

        if "battery" in self._sensor:
            value = 0
            for row in self.device_coordinator.data:
                if str(row.device_id) in self._sensor:
                    value = row.battery
                    break
        elif SENSOR_TYPES[self._sensor][SENSOR_DEVICE_CLASS] == DEVICE_CLASS_PRESSURE:
            value = getattr(self.coordinator.data[SENSOR_NAME], self._sensor, None)
            if value is not None:
                if self._unit_system == "imperial":
                    return round(value, 3)
                return round(value, 2)
        elif self._sensor == "station_information":
            value = self._station_info.get("station_name")
        else:
            value = getattr(self.coordinator.data[0], self._sensor, None)
            if not isinstance(value, str) and value is not None:
                if SENSOR_TYPES[self._sensor][SENSOR_IGNORE_ZERO] and value == 0:
                    return None
                return round(value, 1)

        return value

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        if SENSOR_TYPES[self._sensor][SENSOR_UNIT] in self._units:
            return self._units[SENSOR_TYPES[self._sensor][SENSOR_UNIT]]

        return SENSOR_TYPES[self._sensor][SENSOR_UNIT]

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return SENSOR_TYPES[self._sensor][SENSOR_ICON]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return SENSOR_TYPES[self._sensor][SENSOR_DEVICE_CLASS]

    @property
    def state_class(self) -> str:
        """State class of sensor."""
        return SENSOR_TYPES[self._sensor][SENSOR_STATE_CLASS]

    @property
    def device_state_attributes(self) -> Dict:
        """Return SmartWeather specific attributes."""
        if "battery" in self._sensor:
            value_type = None
            for row in self.device_coordinator.data:
                if str(row.device_id) in self._sensor:
                    value_type = row.device_type_desc
                    break

            return {
                ATTR_DEVICE_TYPE: value_type,
                ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
                ATTR_SMARTWEATHER_STATION_ID: self._device_key,
            }
        elif self._sensor == "station_information":
            return self._station_info
        else:
            return {
                ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
                ATTR_SMARTWEATHER_STATION_ID: self._device_key,
            }

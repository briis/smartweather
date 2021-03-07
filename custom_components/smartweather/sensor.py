"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create sensors for each type.

    For a full description, go here: https://github.com/briis/smartweather

    Author: Bjarne Riis
"""
import logging
from typing import Dict

from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
import homeassistant.helpers.device_registry as dr
from homeassistant.util import slugify
from .const import (
    ATTR_DEVICE_TYPE,
    ATTR_SMARTWEATHER_STATION_ID,
    DEFAULT_ATTRIBUTION,
    DOMAIN,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
    CONF_ADD_SENSORS,
)
from .entity import SmartWeatherEntity

_LOGGER = logging.getLogger(__name__)

# Sensor types are defined like: Name, Unit Type, icon, device class, Ignore on 0 Value
SENSOR_TYPES = {
    "air_temperature": [
        "Temperature",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        False,
    ],
    "air_density": [
        "Air Density",
        "kg/m3",
        "mdi:weight-kilogram",
        None,
        False,
    ],
    "feels_like": [
        "Feels Like",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        False,
    ],
    "heat_index": [
        "Heat Index",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        False,
    ],
    "wind_chill": [
        "Wind Chill",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        False,
    ],
    "dew_point": [
        "Dewpoint",
        UNIT_TYPE_TEMP,
        "mdi:thermometer",
        DEVICE_CLASS_TEMPERATURE,
        False,
    ],
    "wind_avg": [
        "Wind Speed",
        UNIT_TYPE_WIND,
        "mdi:weather-windy",
        None,
        False,
    ],
    "wind_bearing": [
        "Wind Bearing",
        "°",
        "mdi:compass-outline",
        None,
        False,
    ],
    "wind_direction": [
        "Wind Direction",
        None,
        "mdi:compass-outline",
        None,
        False,
    ],
    "wind_gust": [
        "Wind Gust",
        UNIT_TYPE_WIND,
        "mdi:weather-windy",
        None,
        False,
    ],
    "precip_accum_local_day": [
        "Rain today",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        False,
    ],
    "precip_rate": [
        "Rain rate",
        UNIT_TYPE_RAIN,
        "mdi:weather-pouring",
        None,
        False,
    ],
    "precip_accum_last_1hr": [
        "Rain last hour",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        False,
    ],
    "precip_accum_local_yesterday": [
        "Rain yesterday",
        UNIT_TYPE_RAIN,
        "mdi:weather-rainy",
        None,
        False,
    ],
    "pressure_trend": [
        "Pressure Trend",
        None,
        "mdi:trending-up",
        None,
        False,
    ],
    "relative_humidity": [
        "Humidity",
        "%",
        "mdi:water-percent",
        DEVICE_CLASS_HUMIDITY,
        True,
    ],
    "station_pressure": [
        "Pressure",
        UNIT_TYPE_PRESSURE,
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
        True,
    ],
    "sea_level_pressure": [
        "Sea Level Pressure",
        UNIT_TYPE_PRESSURE,
        "mdi:gauge",
        DEVICE_CLASS_PRESSURE,
        True,
    ],
    "uv": [
        "UV",
        "UV",
        "mdi:weather-sunny",
        None,
        False,
    ],
    "solar_radiation": [
        "Solar Radiation",
        "W/m2",
        "mdi:solar-power",
        None,
        False,
    ],
    "brightness": [
        "Brightness",
        "Lx",
        "mdi:brightness-5",
        DEVICE_CLASS_ILLUMINANCE,
        False,
    ],
    "lightning_strike_count": [
        "Lightning Count",
        None,
        "mdi:weather-lightning",
        None,
        False,
    ],
    "lightning_strike_last_distance": [
        "Lightning Distance",
        UNIT_TYPE_DISTANCE,
        "mdi:weather-lightning",
        None,
        False,
    ],
    "lightning_strike_last_time": [
        "Lightning Time",
        "",
        "mdi:clock-outline",
        "timestamp",
        False,
    ],
    "lightning_strike_count_last_1hr": [
        "Lightning Last 1Hrs",
        "",
        "mdi:history",
        None,
        False,
    ],
    "lightning_strike_count_last_3hr": [
        "Lightning Last 3Hrs",
        "",
        "mdi:history",
        None,
        False,
    ],
    "precip_minutes_local_day": [
        "Rain minutes today",
        "min",
        "mdi:timer-outline",
        None,
        False,
    ],
    "precip_minutes_local_yesterday": [
        "Rain minutes yesterday",
        "min",
        "mdi:timer-outline",
        None,
        False,
    ],
}


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:

    # Exit if user did deselect sensors and alerts on config
    if not entry.data[CONF_ADD_SENSORS]:
        return

    """Set up the Meteobridge sensor platform."""
    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    device_coordinator = hass.data[DOMAIN][entry.entry_id]["device_coordinator"]
    if not device_coordinator.data:
        return

    smartweather = hass.data[DOMAIN][entry.entry_id]["smw"]
    if not smartweather:
        return
    units = await smartweather.get_units()

    station_info = hass.data[DOMAIN][entry.entry_id]["station"]
    if not station_info:
        return

    for sensor in device_coordinator.data:
        # Append Batteri Devices to SENSOR_TYPES
        key = f"battery_{sensor.device_type_desc}_{sensor.device_id}"
        SENSOR_TYPES.setdefault(key, [])
        SENSOR_TYPES[key] = [
            f"Battery {sensor.device_name}",
            "V",
            "mdi:battery",
            DEVICE_CLASS_VOLTAGE,
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
            )
        )
        _LOGGER.debug(f"SENSOR ADDED: {sensor}")

    async_add_entities(sensors, True)
    return True


class SmartWeatherSensor(SmartWeatherEntity, Entity):
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
        self._sensor = sensor
        self._state = None
        self._name = f"{DOMAIN.capitalize()} {SENSOR_TYPES[self._sensor][0]}"

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
        else:
            value = getattr(self.coordinator.data[0], self._sensor, None)
            if not isinstance(value, str) and value is not None:
                if SENSOR_TYPES[self._sensor][4] and value == 0:
                    return
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
        else:
            return {
                ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
                ATTR_SMARTWEATHER_STATION_ID: self._device_key,
            }

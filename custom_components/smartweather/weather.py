"""Support for the SmartWeather weather service."""
import logging
from typing import Dict, List
from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED,
    WeatherEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ID,
    LENGTH_METERS,
    LENGTH_MILES,
    LENGTH_KILOMETERS,
    PRESSURE_HPA,
    PRESSURE_INHG,
    TEMP_CELSIUS,
)
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util.distance import convert as convert_distance
from homeassistant.util.pressure import convert as convert_pressure
import homeassistant.helpers.device_registry as dr
from .const import (
    DOMAIN,
    ATTR_STATION_NAME,
    ATTR_UPDATED,
    ATTR_STATION_ID,
    ATTR_CURRENT_ICON,
    ATTR_FCST_POP,
    ATTR_FCST_UV,
    DEFAULT_ATTRIBUTION,
    DEVICE_TYPE_WEATHER,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
    CONDITION_CLASSES,
    CONF_STATION_ID,
    CONF_FORECAST_TYPE,
)
from .entity import SmartWeatherEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistantType, entry: ConfigEntry, async_add_entities
) -> None:
    """Add a weather entity from station_id."""

    unit_system = "metric" if hass.config.units.is_metric else "imperial"

    fcst_coordinator = hass.data[DOMAIN][entry.entry_id]["fcst_coordinator"]
    if not fcst_coordinator.data:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    if not coordinator.data:
        return

    station_info = hass.data[DOMAIN][entry.entry_id]["station"]
    if not station_info:
        return

    fcst_type = hass.data[DOMAIN][entry.entry_id]["fcst_type"]
    if not fcst_type:
        return

    weather_entity = SmartWeatherWeather(
        coordinator,
        entry.data,
        DEVICE_TYPE_WEATHER,
        station_info,
        fcst_coordinator,
        unit_system,
        fcst_type,
    )

    async_add_entities([weather_entity], True)

    return True


class SmartWeatherWeather(SmartWeatherEntity, WeatherEntity):
    """Representation of a weather entity."""

    def __init__(
        self,
        coordinator,
        entries,
        device_type,
        server,
        fcst_coordinator,
        unit_system,
        fcst_type,
    ) -> None:
        """Initialize the SmartWeather weather entity."""
        super().__init__(coordinator, entries, device_type, server, fcst_coordinator)
        self._name = f"{DOMAIN.capitalize()} {entries[CONF_ID]}"
        self._station_id = entries[CONF_STATION_ID]
        self._unit_system = unit_system
        self._forecast_type = fcst_type

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def temperature(self) -> int:
        """Return the temperature."""
        if self._current is not None:
            # Current Temperature is in Fahrenheit if Units is Imperial
            # we need to convert back to C, as HA also is converting
            if self._unit_system == "imperial":
                return (self._current.air_temperature - 32) / 1.8
            else:
                return self._current.air_temperature
        return None

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def humidity(self) -> int:
        """Return the humidity."""
        if self._current is not None:
            return self._current.relative_humidity
        return None

    @property
    def wind_speed(self) -> float:
        """Return the wind speed."""
        if self._current is not None:
            return self._current.wind_avg
        return None

    @property
    def wind_gust(self) -> float:
        """Return the wind Gust."""
        if self._current is not None:
            return self._current.wind_gust
        return None

    @property
    def wind_bearing(self) -> int:
        """Return the wind bearing."""
        if self._current is not None:
            return self._current.wind_bearing
        return None

    @property
    def precipitation(self) -> float:
        """Return the precipitation."""
        if self._current is not None:
            return self._current.precip_accum_local_day
        return None

    @property
    def pressure(self) -> int:
        """Return the pressure."""
        if self._current is not None:
            return round(self._current.station_pressure, 2)
        return None

    @property
    def uv(self) -> int:
        """Return the UV Index."""
        if self._current is not None:
            return round(self._current.uv, 1)
        return None

    @property
    def current_condition(self) -> int:
        """Return Current Condition Icon."""
        if self._forecast is not None:
            return self._forecast.current_icon
        return None

    @property
    def condition(self) -> str:
        """Return the weather condition."""
        return next(
            (k for k, v in CONDITION_CLASSES.items() if self.current_condition in v),
            None,
        )

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return DEFAULT_ATTRIBUTION

    @property
    def device_state_attributes(self) -> Dict:
        """Return Weatherbit specific attributes."""
        return {
            ATTR_STATION_ID: self._station_id,
            ATTR_CURRENT_ICON: self.current_condition,
            ATTR_FCST_UV: self.uv,
        }

    @property
    def forecast(self) -> List:
        """Return the forecast."""
        if self.fcst_coordinator.data is None or len(self.fcst_coordinator.data) < 2:
            return None

        data = []

        for forecast in self.fcst_coordinator.data:
            condition = next(
                (k for k, v in CONDITION_CLASSES.items() if forecast.icon in v), None,
            )

            if self._forecast_type == FORECAST_TYPE_DAILY:
                data.append(
                    {
                        ATTR_FORECAST_TIME: forecast.timestamp,
                        ATTR_FORECAST_TEMP: forecast.temp_high,
                        ATTR_FORECAST_TEMP_LOW: forecast.temp_low,
                        ATTR_FORECAST_PRECIPITATION: forecast.precip,
                        ATTR_FCST_POP: forecast.precip_probability,
                        ATTR_FORECAST_CONDITION: condition,
                        ATTR_FORECAST_WIND_SPEED: forecast.wind_avg,
                        ATTR_FORECAST_WIND_BEARING: forecast.wind_bearing,
                        "icon": forecast.icon,  # REMOVE when we know all icons
                    }
                )
            else:
                data.append(
                    {
                        ATTR_FORECAST_TIME: forecast.timestamp,
                        ATTR_FORECAST_TEMP: forecast.temperature,
                        ATTR_FORECAST_PRECIPITATION: forecast.precip,
                        ATTR_FCST_POP: forecast.precip_probability,
                        ATTR_FORECAST_CONDITION: condition,
                        ATTR_FORECAST_WIND_SPEED: forecast.wind_avg,
                        ATTR_FORECAST_WIND_BEARING: forecast.wind_bearing,
                        "icon": forecast.icon,  # REMOVE when we know all icons
                    }
                )

        return data

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.fcst_coordinator.async_add_listener(self.async_write_ha_state)
        )

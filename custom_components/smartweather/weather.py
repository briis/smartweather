"""Support for the SmartWeather weather service."""
import logging
from typing import List
from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    WeatherEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ID,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import utc_from_timestamp
from homeassistant.util.temperature import celsius_to_fahrenheit

from pysmartweatherio import FORECAST_TYPE_DAILY
from .const import (
    DOMAIN,
    ATTR_CURRENT_ICON,
    ATTR_FCST_UV,
    ATTR_TEMP_HIGH_TODAY,
    ATTR_TEMP_LOW_TODAY,
    DEFAULT_ATTRIBUTION,
    DEVICE_TYPE_WEATHER,
    CONDITION_CLASSES,
)
from .entity import SmartWeatherEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
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
        super().__init__(
            coordinator, entries, device_type, server, fcst_coordinator, None
        )
        self._name = f"{DOMAIN.capitalize()} {entries[CONF_ID]}"
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
            return round(self._current.precip_accum_local_day, 1)
        return None

    @property
    def pressure(self) -> int:
        """Return the pressure."""
        if self._current is not None:
            if self._unit_system == "imperial":
                return round(self._current.sea_level_pressure, 3)
            return round(self._current.sea_level_pressure, 2)
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
    def temp_high_today(self) -> float:
        """Return Todays High Temp Forecast."""
        if self._forecast is not None:
            if self._unit_system == "imperial":
                return celsius_to_fahrenheit(self._forecast.temp_high_today)
            return self._forecast.temp_high_today
        return None

    @property
    def temp_low_today(self) -> float:
        """Return Todays Low Temp Forecast."""
        if self._forecast is not None:
            if self._unit_system == "imperial":
                return celsius_to_fahrenheit(self._forecast.temp_low_today)
            return self._forecast.temp_low_today
        return None

    @property
    def attribution(self) -> str:
        """Return the attribution."""
        return DEFAULT_ATTRIBUTION

    @property
    def extra_state_attributes(self):
        """Return the sensor state attributes."""
        return {
            **super().extra_state_attributes,
            ATTR_CURRENT_ICON: self.current_condition,
            ATTR_FCST_UV: self.uv,
            ATTR_WEATHER_HUMIDITY: self.humidity,
            ATTR_WEATHER_PRESSURE: self.pressure,
            ATTR_WEATHER_TEMPERATURE: self.temperature,
            ATTR_WEATHER_WIND_BEARING: self.wind_bearing,
            ATTR_WEATHER_WIND_SPEED: self.wind_speed,
            ATTR_TEMP_HIGH_TODAY: self.temp_high_today,
            ATTR_TEMP_LOW_TODAY: self.temp_low_today,
        }

    @property
    def forecast(self) -> List:
        """Return the forecast."""
        if self.fcst_coordinator.data is None or len(self.fcst_coordinator.data) < 2:
            return None

        data = []

        for forecast in self.fcst_coordinator.data:
            condition = next(
                (k for k, v in CONDITION_CLASSES.items() if forecast.icon in v),
                None,
            )

            if self._forecast_type == FORECAST_TYPE_DAILY:
                data.append(
                    {
                        ATTR_FORECAST_TIME: utc_from_timestamp(
                            forecast.epochtime
                        ).isoformat(),
                        ATTR_FORECAST_TEMP: forecast.temp_high,
                        ATTR_FORECAST_TEMP_LOW: forecast.temp_low,
                        ATTR_FORECAST_PRECIPITATION: round(forecast.precip, 1)
                        if forecast.precip is not None
                        else None,
                        ATTR_FORECAST_PRECIPITATION_PROBABILITY: forecast.precip_probability,
                        ATTR_FORECAST_CONDITION: condition,
                        ATTR_FORECAST_WIND_SPEED: forecast.wind_avg,
                        ATTR_FORECAST_WIND_BEARING: forecast.wind_bearing,
                    }
                )
            else:
                data.append(
                    {
                        ATTR_FORECAST_TIME: utc_from_timestamp(
                            forecast.epochtime
                        ).isoformat(),
                        ATTR_FORECAST_TEMP: forecast.temperature,
                        ATTR_FORECAST_PRECIPITATION: round(forecast.precip, 1)
                        if forecast.precip is not None
                        else None,
                        ATTR_FORECAST_PRECIPITATION_PROBABILITY: forecast.precip_probability,
                        ATTR_FORECAST_CONDITION: condition,
                        ATTR_FORECAST_WIND_SPEED: forecast.wind_avg,
                        ATTR_FORECAST_WIND_BEARING: forecast.wind_bearing,
                    }
                )

        return data

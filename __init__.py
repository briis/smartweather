
"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component connects to the REST API of WeatherFlow and
    retieves the data, that is then consumed by the Sensors

    For a full description, go here: https://github.com/briis/hass-SmartWeather

    Author: Bjarne Riis

"""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (CONF_NAME, CONF_API_KEY)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION, ATTR_FORECAST_PRECIPITATION, ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW, ATTR_FORECAST_TIME, ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_WIND_SPEED, PLATFORM_SCHEMA, WeatherEntity)
from homeassistant.helpers.temperature import display_temp as show_temp
from homeassistant.const import (PRECISION_TENTHS, PRECISION_WHOLE, TEMP_CELSIUS)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'smartweather'
DATA_SMARTWEATHER = 'SmartWeather'
CONF_STATION_ID = 'station_id'

ATTRIBUTION = 'Weather data powered by a SmartWeather Weather Station'

ATTR_CONDITION_CLASS = 'condition_class'
ATTR_FORECAST = 'forecast'
ATTR_FORECAST_CONDITION = 'condition'
ATTR_FORECAST_PRECIPITATION = 'precipitation'
ATTR_FORECAST_TEMP = 'temperature'
ATTR_FORECAST_TEMP_LOW = 'templow'
ATTR_FORECAST_TIME = 'datetime'
ATTR_FORECAST_WIND_BEARING = 'wind_bearing'
ATTR_FORECAST_WIND_SPEED = 'wind_speed'
ATTR_WEATHER_ATTRIBUTION = 'attribution'
ATTR_WEATHER_HUMIDITY = 'humidity'
ATTR_WEATHER_OZONE = 'ozone'
ATTR_WEATHER_PRESSURE = 'pressure'
ATTR_WEATHER_TEMPERATURE = 'temperature'
ATTR_WEATHER_VISIBILITY = 'visibility'
ATTR_WEATHER_WIND_BEARING = 'wind_bearing'
ATTR_WEATHER_WIND_SPEED = 'wind_speed'
ATTR_WEATHER_WIND_GUST = 'wind_gust'
ATTR_WEATHER_DEWPOINT = 'dewpoint'
ATTR_WEATHER_FEELS_LIKE = 'feels_like'
ATTR_WEATHER_PRECIPITATION = 'precipitation'
ATTR_WEATHER_PRECIPITATION_RATE = 'precipitation_rate'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

SCAN_INTERVAL = timedelta(seconds=60)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_STATION_ID): cv.string,
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional(CONF_NAME, default=DATA_SMARTWEATHER): cv.string
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Set up the SmartWeather platform."""

    if hass.config.units.is_metric:
        unit_system = 'metric'
    else:
        unit_system = 'imperial'

    stationid = config[DOMAIN].get(CONF_STATION_ID)
    api_key = config[DOMAIN].get(CONF_API_KEY)
    name = config[DOMAIN].get(CONF_NAME)
    data = SmartWeatherCurrentData(hass, stationid, unit_system, api_key)
    data.update()

    if data.data.timestamp is None:
        return False

    hass.data[DATA_SMARTWEATHER] = data
    hass.data[CONF_NAME] = name

    return True

class SmartWeatherCurrentData:
    """ Get the current data from the Weatherstation """

    def __init__(self, hass, station_id, unit_system, api_key):
        """Initialize the data object."""
        self._station_id = station_id
        self._unit_system = unit_system
        self._api_key = api_key
        self.data = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from the Weatherstation."""
        from .smartweatherio import load_weatherdata as lw

        try:
            weather = lw(self._station_id, self._api_key, self._unit_system)
            self.data = weather.currentdata()
        except (ValueError) as err:
            _LOGGER.error("Check SmartWeather error %s", err.args)
            self.data = None

class WeatherEntityExtended(Entity):
    """ABC for weather data."""

    @property
    def temperature(self):
        """Return the platform temperature."""
        raise NotImplementedError()

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        raise NotImplementedError()

    @property
    def pressure(self):
        """Return the pressure."""
        return None

    @property
    def humidity(self):
        """Return the humidity."""
        raise NotImplementedError()

    @property
    def wind_speed(self):
        """Return the wind speed."""
        return None

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return None

    @property
    def ozone(self):
        """Return the ozone level."""
        return None

    @property
    def attribution(self):
        """Return the attribution."""
        return None

    @property
    def visibility(self):
        """Return the visibility."""
        return None

    @property
    def forecast(self):
        """Return the forecast."""
        return None

    @property
    def precision(self):
        """Return the forecast."""
        return PRECISION_TENTHS if self.temperature_unit == TEMP_CELSIUS \
            else PRECISION_WHOLE

    @property
    def state_attributes(self):
        """Return the state attributes."""
        data = {
            ATTR_WEATHER_TEMPERATURE: show_temp(
                self.hass, self.temperature, self.temperature_unit,
                self.precision),
        }

        humidity = self.humidity
        if humidity is not None:
            data[ATTR_WEATHER_HUMIDITY] = round(humidity)

        dewpoint = self.dewpoint
        if dewpoint is not None:
            data[ATTR_WEATHER_DEWPOINT] = dewpoint

        feels_like = self.feels_like
        if feels_like is not None:
            data[ATTR_WEATHER_FEELS_LIKE] = feels_like

        ozone = self.ozone
        if ozone is not None:
            data[ATTR_WEATHER_OZONE] = ozone

        precipitation = self.precipitation
        if precipitation is not None:
            data[ATTR_WEATHER_PRECIPITATION] = precipitation

        precipitation_rate = self.precipitation_rate
        if precipitation_rate is not None:
            data[ATTR_WEATHER_PRECIPITATION_RATE] = precipitation_rate

        pressure = self.pressure
        if pressure is not None:
            data[ATTR_WEATHER_PRESSURE] = pressure

        wind_bearing = self.wind_bearing
        if wind_bearing is not None:
            data[ATTR_WEATHER_WIND_BEARING] = wind_bearing

        wind_speed = self.wind_speed
        if wind_speed is not None:
            data[ATTR_WEATHER_WIND_SPEED] = wind_speed

        wind_gust= self.wind_gust
        if wind_gust is not None:
            data[ATTR_WEATHER_WIND_GUST] = wind_gust

        visibility = self.visibility
        if visibility is not None:
            data[ATTR_WEATHER_VISIBILITY] = visibility

        attribution = self.attribution
        if attribution is not None:
            data[ATTR_WEATHER_ATTRIBUTION] = attribution

        if self.forecast is not None:
            forecast = []
            for forecast_entry in self.forecast:
                forecast_entry = dict(forecast_entry)
                forecast_entry[ATTR_FORECAST_TEMP] = show_temp(
                    self.hass, forecast_entry[ATTR_FORECAST_TEMP],
                    self.temperature_unit, self.precision)
                if ATTR_FORECAST_TEMP_LOW in forecast_entry:
                    forecast_entry[ATTR_FORECAST_TEMP_LOW] = show_temp(
                        self.hass, forecast_entry[ATTR_FORECAST_TEMP_LOW],
                        self.temperature_unit, self.precision)
                forecast.append(forecast_entry)

            data[ATTR_FORECAST] = forecast

        return data

    @property
    def state(self):
        """Return the current state."""
        return self.condition

    @property
    def condition(self):
        """Return the current condition."""
        raise NotImplementedError()

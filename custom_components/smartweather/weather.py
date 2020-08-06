"""
    Support for the SmartWeather Weatherstation from WeatherFlow
    This component will read the local or public weatherstation data
    and create sensors for each type.
    Support for retrieving meteorological data from Tempest SmartWeather API (beta).

    For a full description, go here: https://github.com/briis/smartweather

    Author: Bjarne Riis
"""
import logging
import sys
import asyncio
import aiohttp
import async_timeout

from datetime import datetime, timedelta
import voluptuous as vol

from requests.exceptions import ConnectionError as ConnectError
from requests.exceptions import HTTPError, Timeout
from homeassistant.util.dt import utc_from_timestamp
import homeassistant.helpers.config_validation as cv
from homeassistant.components.weather import (ATTR_FORECAST_CONDITION,
                                              ATTR_FORECAST_PRECIPITATION,
                                              ATTR_FORECAST_PRECIPITATION_PROBABILITY,
                                              ATTR_FORECAST_TEMP,
                                              ATTR_FORECAST_TEMP_LOW,
                                              ATTR_FORECAST_TIME,
                                              ATTR_FORECAST_WIND_BEARING,
                                              ATTR_FORECAST_WIND_SPEED,
                                              PLATFORM_SCHEMA)
from homeassistant.const import (CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE,
                                 CONF_MODE, CONF_NAME, TEMP_CELSIUS,
                                 TEMP_FAHRENHEIT)
from homeassistant.util import Throttle

from . import DATA_SMARTWEATHER, WeatherEntityExtended

DEPENDENCIES = ['smartweather']

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Powered by SmartWeather Weather Station"

FORECAST_MODE = ['hourly', 'daily']

MAP_CONDITION = {
    'clear-day': 'sunny',
    'clear-night': 'clear-night',
    'rain': 'rainy',
    'snow': 'snowy',
    'sleet': 'snowy-rainy',
    'wind': 'windy',
    'fog': 'fog',
    'cloudy': 'cloudy',
    'partly-cloudy-day': 'partlycloudy',
    'partly-cloudy-night': 'partlycloudy',
    'hail': 'hail',
    'thunderstorm': 'lightning',
    'tornado': None,
}

CONF_UNITS = 'units'

DEFAULT_NAME = 'smartweather'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_API_KEY): cv.string,
    vol.Optional(CONF_LATITUDE): cv.latitude,
    vol.Optional(CONF_LONGITUDE): cv.longitude,
    vol.Optional(CONF_MODE, default='hourly'): vol.In(FORECAST_MODE),
    vol.Optional(CONF_UNITS): vol.In(['auto', 'si', 'us', 'ca', 'uk', 'uk2']),
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=3)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Tempest SmartWeather weather entity."""
    _LOGGER.debug('SmartWeather setup_platform()')

    # latitude = config.get(CONF_LATITUDE, hass.config.latitude)
    # longitude = config.get(CONF_LONGITUDE, hass.config.longitude)
    # name = config.get(CONF_NAME)
    # mode = config.get(CONF_MODE)
    # sw_currently = hass.data[DATA_SMARTWEATHER]
    data = hass.data[DATA_SMARTWEATHER]    
    name = config.get(CONF_NAME)
    units = config.get(CONF_UNITS)
    # data = hass.data[DATA_SMARTWEATHER]
    # wind_unit = config.get(CONF_WIND_UNIT)

    #_LOGGER.info("Weather API Key: " + config.get(CONF_API_KEY))
    
    # if not units:
    #     units = 'ca' if hass.config.units.is_metric else 'us'

    add_entities([TempestWeather(data)], True)

class TempestWeather(WeatherEntityExtended):
    """ Representation of Tempest weather data """

    def __init__(self, data, name='Tempest'):
        """ Initialize """
        _LOGGER.debug('TempestWeather init()')
        self._name = name
        self._data = data
        _LOGGER.debug(f'Smartweather initialized w/ Data:\n {data.observations}\n{data.forecast_current_conditions}')
        # Mapping between tempest & hass conditions
        self.CONDITIONS_MAP = {
            "clear-night": [],
            "cloudy": ["cloudy"],
            "exceptional": [],
            "fog": ["foggy", "fog"],
            "hail": ["hail"],
            "lightning": [],
            "lightning-rainy": [],
            "partlycloudy": ["partly cloudy"],
            "pouring": ["raining"],
            "rainy": ["rain possible"],
            "snowy": ["snowy"],
            "snowy-rainy": [],
            "sunny": ["clear"],
            "windy": ["windy"],
            "windy-variant": [ ]
        }

        # Example from observations's obs:
            # "obs": [
            #     {
            #         "timestamp": 1596733459,
            #         "air_temperature": 18.6,
            #         "barometric_pressure": 1007.3,
            #         "station_pressure": 1007.3,
            #         "sea_level_pressure": 1014.1,
            #         "relative_humidity": 74,
            #         "precip": 0,
            #         "precip_accum_last_1hr": 0,
            #         "precip_accum_local_day": 0,
            #         "precip_accum_local_yesterday": 0.000595,
            #         "precip_accum_local_yesterday_final": 0,
            #         "precip_minutes_local_day": 0,
            #         "precip_minutes_local_yesterday": 1,
            #         "precip_minutes_local_yesterday_final": 0,
            #         "precip_analysis_type_yesterday": 1,
            #         "wind_avg": 0.6,
            #         "wind_direction": 98,
            #         "wind_gust": 1.3,
            #         "wind_lull": 0,
            #         "solar_radiation": 881,
            #         "uv": 6.7,
            #         "brightness": 105690,
            #         "lightning_strike_count": 0,
            #         "lightning_strike_count_last_1hr": 0,
            #         "lightning_strike_count_last_3hr": 0,
            #         "feels_like": 18.6,
            #         "heat_index": 18.6,
            #         "wind_chill": 18.6,
            #         "dew_point": 13.9,
            #         "wet_bulb_temperature": 15.7,
            #         "delta_t": 2.9,
            #         "air_density": 1.20276
            #     }
            # ]

        self.OBSERVATIONS_MAP = {
            # HASS Weather Property >> Tempest Property
            'precipitation': 'precip',
            'temperature': 'air_temperature',
            'precipitation_rate': 'precip_accum_last_1hr', # TODO: Confirm timescale for rate here (maybe not 1h)
            'humidity': 'relative_humidity',
            'dewpoint': 'dew_point',
            'wind_speed': 'wind_avg',
            'wind_bearing': 'wind_direction',
            'pressure': 'station_pressure'
        }

        # Excluding the conditions that are duplicative from observations API
        self.FORECAST_CURRENT_CONDITIONS_MAP = {
            # HASS Weather Property >> Tempest Property
            'conditions': 'conditions',
            'icon': 'icon',
            'pressure_trend': 'pressure_trend',
            'wind_direction_cardinal': 'wind_direction_cardinal',
            'wind_direction_icon': 'wind_direction_icon',
            'is_precip_local_day_rain_check': 'is_precip_local_day_rain_check',
            'is_precip_local_yesterday_rain_check': 'is_precip_local_yesterday_rain_check'
        }

    def __getattr__(self, name):
        # Because hass/core uses hasattr()
        #if name == "async_update": return False

        # Catch all generic attributes where we only need to return the value.
        if name in self._data.observations:
            return self._data.observations[name]
        elif name in self.OBSERVATIONS_MAP: 
            return self._data.observations[self.OBSERVATIONS_MAP[name]]
        if name in self._data.forecast_current_conditions: 
            return self._data.forecast_current_conditions[name]
        elif name in self.FORECAST_CURRENT_CONDITIONS_MAP: 
            return self._data.forecast_current_conditions[self.FORECAST_CURRENT_CONDITIONS_MAP[name]]
        else:
            _LOGGER.warning(f'smartweather queried for missing property: {name}')
            #raise NotImplementedError()
            return self.__getattribute__(name)

    def update(self):
        """Get the latest weather data."""
        return self._data.update()

    # Weather Properties Below

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """ 
            No idea what this does so let's go with no 
            TODO: Read this sometime: https://developers.home-assistant.io/docs/integration_fetching_data/
        """
        return False

    @property
    def condition(self):
        """Return the weather condition."""
        # TODO: Need to check 'precip_type' in forecast data to find out if non-rain precip.
        return self._hass_condition(self.conditions)

    def _hass_condition(self, tempest_condition_name):
        """ Returns HASS Condition that maps to the tempest condition name -- case insensitive """
        return [
            k for k, v in self.CONDITIONS_MAP.items() if tempest_condition_name.lower() in v
        ][0]

    @property
    def attribution(self):
        """Return the attribution."""
        return "Powered by Home Assistant & Tempest Weather Station"

    @property
    def forecast(self):
        """Return the forecast."""        
        forecast_data = []
        daily_forcasts = iter(self._data.forecast['daily'])
        next(daily_forcasts) # Don't want forcast for today

        for entry in daily_forcasts:
            # First, calculate data from hourly that's not summed up in the daily.
            precip = 0
            wind_avg = []
            wind_bearing = []
            
            for hourly in self._data.forecast['hourly']:
                if hourly['local_day'] == entry['day_num']:
                    precip += hourly['precip']
                    wind_avg.append(hourly['wind_avg'])
                    wind_bearing.append(hourly['wind_direction'])
            
            data_dict = {
                ATTR_FORECAST_TIME: utc_from_timestamp(entry['day_start_local']).isoformat(),
                ATTR_FORECAST_CONDITION: self._hass_condition(entry['conditions']),
                ATTR_FORECAST_PRECIPITATION_PROBABILITY: entry['precip_probability'],
                ATTR_FORECAST_TEMP: entry['air_temp_high'],
                ATTR_FORECAST_TEMP_LOW: entry['air_temp_low'],
                ATTR_FORECAST_WIND_BEARING: sum(wind_bearing) / len(wind_bearing),
                ATTR_FORECAST_WIND_SPEED: sum(wind_avg) / len(wind_avg),
                ATTR_FORECAST_PRECIPITATION: precip,
                # TODO: What is this?
                # ATTR_FORECAST = "forecast" ?
            }
            forecast_data.append(data_dict)

        return forecast_data

        # EXAMPLE: Daily forecast 
            # {
            #     "day_start_local": 1596438000,
            #     "day_num": 3,
            #     "month_num": 8,
            #     "conditions": "Cloudy",
            #     "icon": "cloudy",
            #     "sunrise": 1596460546,
            #     "sunset": 1596510932,
            #     "air_temp_high": 19,
            #     "air_temp_low": 12,
            #     "air_temp_high_color": "dbde00",
            #     "air_temp_low_color": "14cb99",
            #     "precip_probability": 10,
            #     "precip_icon": "chance-rain",
            #     "precip_type": "rain"
            # }

        # EXAMPLE: Hourly forecast - self._data.forecast['hourly']
            # {
            #     "time": 1596517200,
            #     "conditions": "Cloudy",
            #     "icon": "cloudy",
            #     "air_temperature": 15,
            #     "sea_level_pressure": 1015.93,
            #     "relative_humidity": 92,
            #     "precip": 0,
            #     "precip_probability": 10,
            #     "precip_type": "rain",
            #     "precip_icon": "chance-rain",
            #     "wind_avg": 7,
            #     "wind_avg_color": "8af822",
            #     "wind_direction": 288,
            #     "wind_direction_cardinal": "WNW",
            #     "wind_direction_icon": "wind-arrow-wnw",
            #     "wind_gust": 8,
            #     "wind_gust_color": "ebf100",
            #     "uv": 0,
            #     "feels_like": 13,
            #     "local_hour": 22,
            #     "local_day": 3
            # }

    ### Properties not currently available from the Tempest ###
    @property
    def ozone(self):
        # Tempest does not provide this.
        return False

    @property
    def visibility(self):
        # Tempest does not provide this. Maybe calculated from air_density?
        return False        
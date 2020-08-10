"""WeatherFlow SmartWeather Integration for Home Assistant"""
import logging
from datetime import timedelta, datetime
import voluptuous as vol

from pysmartweatherio import (
    SmartWeather,
    SmartWeatherError,
    InvalidApiKey,
    RequestError,
    ResultError,
)

from homeassistant.const import (
    CONF_ID,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers import update_coordinator

from .const import (
    DOMAIN,
    CONF_STATION_ID,
    CONF_WIND_UNIT,
    SMARTWEATHER_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured SmartWeather."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up SmartWeather platforms as config entry."""

    unit_system = "metric" if hass.config.units.is_metric else "imperial"
    session = async_get_clientsession(hass)

    smartweather = SmartWeather(
        entry.data[CONF_API_KEY],
        entry.data[CONF_STATION_ID],
        unit_system,
        entry.data[CONF_WIND_UNIT],
        session,
    )
    _LOGGER.debug("Connected to SmartWeather Platform")

    unique_id = entry.data[CONF_ID]

    hass.data.setdefault(DOMAIN, {})[unique_id] = smartweather

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=smartweather.get_station_data,
        update_interval=SCAN_INTERVAL,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data[DOMAIN][entry.data[CONF_ID]] = {
        "coordinator": coordinator,
        "smw": smartweather,
    }

    for platform in SMARTWEATHER_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload Unifi Protect config entry."""
    for platform in SMARTWEATHER_PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, platform)

    del hass.data[DOMAIN][entry.data[CONF_ID]]

    return True

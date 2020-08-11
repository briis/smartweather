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

import homeassistant.helpers.device_registry as dr
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp.client_exceptions import ServerDisconnectedError
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_STATION_ID,
    CONF_ADD_SENSORS,
    CONF_WIND_UNIT,
    DEFAULT_SCAN_INTERVAL,
    SMARTWEATHER_PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)

# SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up configured SmartWeather."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Set up SmartWeather platforms as config entry."""

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_ADD_SENSORS: entry.data.get(CONF_ADD_SENSORS, True),
                CONF_SCAN_INTERVAL: entry.data.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                ),
            },
        )

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

    # unique_id = entry.data[CONF_ID]

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = smartweather

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=smartweather.get_station_data,
        update_interval=timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )

    try:
        station_info = await smartweather.get_station_hardware()
    except InvalidApiKey:
        _LOGGER.error(
            "Could not Authorize against Weatherflow Server. Please reinstall integration."
        )
        return
    except (ResultError, ServerDisconnectedError) as err:
        _LOGGER.warning(str(err))
        raise ConfigEntryNotReady
    except RequestError as err:
        _LOGGER.error(f"Error occured: {err}")
        return

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()
    hass.data[DOMAIN][entry.data[CONF_ID]] = {
        "coordinator": coordinator,
        "smw": smartweather,
        "station": station_info,
    }

    await _async_get_or_create_smartweather_device_in_registry(
        hass, entry, station_info
    )

    for platform in SMARTWEATHER_PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    if not entry.update_listeners:
        entry.add_update_listener(async_update_options)

    return True


async def _async_get_or_create_smartweather_device_in_registry(
    hass: HomeAssistantType, entry: ConfigEntry, svr
) -> None:
    device_registry = await dr.async_get_registry(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, svr["serial_number"])},
        identifiers={(DOMAIN, svr["serial_number"])},
        manufacturer=DEFAULT_BRAND,
        name=svr["station_name"],
        model=svr["device_id"],
        sw_version=svr["firmware_revision"],
    )


async def async_update_options(hass: HomeAssistantType, entry: ConfigEntry):
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    """Unload Unifi Protect config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in SMARTWEATHER_PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

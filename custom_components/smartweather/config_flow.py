""" Config Flow to configure SmartWeather Integration. """
import logging

from pysmartweatherio import (
    SmartWeather,
    SmartWeatherError,
    InvalidApiKey,
    RequestError,
    ResultError,
)

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_ID,
    CONF_API_KEY,
    CONF_SCAN_INTERVAL,
)

from homeassistant.helpers import aiohttp_client
from homeassistant import config_entries, core
import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback
from homeassistant.util import slugify

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_FORECAST_INTERVAL,
    CONF_STATION_ID,
    CONF_WIND_UNIT,
    CONF_ADD_SENSORS,
    CONF_FORECAST_TYPE,
    CONF_FORECAST_INTERVAL,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
    FORECAST_TYPES,
    UNIT_WIND_MS,
    WIND_UNITS,
)

_LOGGER = logging.getLogger(__name__)


class SmartWeatherFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a SmartWeather config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is None:
            return await self._show_setup_form(user_input)

        errors = {}

        unit_system = "metric" if self.hass.config.units.is_metric else "imperial"
        session = aiohttp_client.async_get_clientsession(self.hass)

        smartweather = SmartWeather(
            user_input[CONF_API_KEY],
            user_input[CONF_STATION_ID],
            unit_system,
            user_input[CONF_WIND_UNIT],
            session,
        )

        try:
            unique_id = await smartweather.get_station_name()
        except InvalidApiKey:
            errors["base"] = "api_error"
            return await self._show_setup_form(errors)
        except ResultError:
            errors["base"] = "station_error"
            return await self._show_setup_form(errors)

        entries = self._async_current_entries()
        for entry in entries:
            if (
                f"{entry.data[CONF_ID]}"
                == f"{unique_id}_{user_input[CONF_FORECAST_TYPE]}"
            ):
                return self.async_abort(reason="station_exists")

        return self.async_create_entry(
            title=f"{unique_id} ({user_input[CONF_FORECAST_TYPE].capitalize()})",
            data={
                CONF_ID: f"{unique_id}_{user_input[CONF_FORECAST_TYPE]}",
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_STATION_ID: user_input[CONF_STATION_ID],
                CONF_FORECAST_TYPE: user_input[CONF_FORECAST_TYPE],
                CONF_ADD_SENSORS: user_input[CONF_ADD_SENSORS],
                CONF_WIND_UNIT: user_input.get(CONF_WIND_UNIT),
                CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL),
                CONF_FORECAST_INTERVAL: user_input.get(CONF_FORECAST_INTERVAL),
            },
        )

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_STATION_ID): int,
                    vol.Required(CONF_ADD_SENSORS, default=True): bool,
                    vol.Optional(
                        CONF_FORECAST_TYPE, default=FORECAST_TYPE_DAILY
                    ): vol.In(FORECAST_TYPES),
                    vol.Optional(CONF_WIND_UNIT, default=UNIT_WIND_MS): vol.In(
                        WIND_UNITS
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=300)),
                    vol.Optional(
                        CONF_FORECAST_INTERVAL, default=DEFAULT_FORECAST_INTERVAL
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                }
            ),
            errors=errors or {},
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_FORECAST_TYPE,
                        default=self.config_entry.options.get(
                            CONF_FORECAST_TYPE, FORECAST_TYPE_DAILY
                        ),
                    ): vol.In(FORECAST_TYPES),
                    vol.Optional(
                        CONF_WIND_UNIT,
                        default=self.config_entry.options.get(
                            CONF_WIND_UNIT, UNIT_WIND_MS
                        ),
                    ): vol.In(WIND_UNITS),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=300)),
                    vol.Optional(
                        CONF_FORECAST_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_FORECAST_INTERVAL, DEFAULT_FORECAST_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                }
            ),
        )

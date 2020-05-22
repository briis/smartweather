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
)

from homeassistant.config_entries import ConfigFlow
from homeassistant.helpers import aiohttp_client
from homeassistant.util import slugify

from .const import (
    DOMAIN,
    CONF_STATION_ID,
    CONF_WIND_UNIT,
    UNIT_WIND_MS,
    WIND_UNITS,
)

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class SmartWeatherFlowHandler(ConfigFlow):
    """Handle a SmartWeather config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def _show_setup_form(self, errors=None):
        """Show the setup form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_STATION_ID): int,
                    vol.Optional(CONF_WIND_UNIT, default=UNIT_WIND_MS): vol.In(
                        WIND_UNITS
                    ),
                }
            ),
            errors=errors or {},
        )

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
            unique_id = slugify(unique_id).capitalize()
            underscore_pos = unique_id.find("_")
            if underscore_pos > 0:
                unique_id = unique_id.split("_")[0]
        except InvalidApiKey:
            errors["base"] = "api_error"
            return await self._show_setup_form(errors)
        except ResultError:
            errors["base"] = "station_error"
            return await self._show_setup_form(errors)

        entries = self._async_current_entries()
        for entry in entries:
            if entry.data[CONF_ID] == unique_id:
                return self.async_abort(reason="station_exists")

        return self.async_create_entry(
            title=unique_id,
            data={
                CONF_ID: unique_id,
                CONF_API_KEY: user_input[CONF_API_KEY],
                CONF_STATION_ID: user_input[CONF_STATION_ID],
                CONF_WIND_UNIT: user_input.get(CONF_WIND_UNIT),
            },
        )

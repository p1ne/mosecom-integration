"""Config flow for Moscow Air Quality Monitoring integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_URL, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_STATION,
    DOMAIN,
)
from .stations import fetch_stations

_LOGGER = logging.getLogger(__name__)


class MosecomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Moscow Air Quality Monitoring."""

    VERSION = 3

    async def async_migrate_entry(self, hass, config_entry: config_entries.ConfigEntry) -> bool:
        """Migrate old entry."""
        _LOGGER.debug("Migrating from version %s", config_entry.version)
        
        if config_entry.version == 1:
            # Version 1 used CONF_URL directly in entry data
            # Version 2+ uses the same format, so no changes needed
            new_data = {**config_entry.data}
            config_entry.version = 2
            hass.config_entries.async_update_entry(config_entry, data=new_data)
        
        if config_entry.version == 2:
            # Version 2 to 3 migration
            # No data changes needed, just version bump
            new_data = {**config_entry.data}
            config_entry.version = 3
            hass.config_entries.async_update_entry(config_entry, data=new_data)

        _LOGGER.info("Migration to version %s successful", config_entry.version)
        return True

    def __init__(self) -> None:
        """Initialize config flow."""
        self.stations: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            # Fetch stations on first load
            self.stations = await fetch_stations(self.hass)
            
            # Build form schema
            data_schema = self._build_form_schema()
            
            return self.async_show_form(
                step_id="user", data_schema=data_schema
            )

        errors = {}

        try:
            # Validate station selection
            if not user_input[CONF_STATION]:
                errors[CONF_STATION] = "station_required"
            else:
                # Check if this URL is already configured
                await self.async_set_unique_id(user_input[CONF_STATION])
                self._abort_if_unique_id_configured()
                
                # Try to fetch data from the URL to validate it works
                from .coordinator import MosecomDataUpdateCoordinator

                coordinator = MosecomDataUpdateCoordinator(
                    self.hass, user_input[CONF_STATION]
                )
                await coordinator.async_refresh()

                if coordinator.last_update_success:
                    # Get available gases from the station
                    available_gases = list(coordinator.data.keys()) if coordinator.data else []
                    
                    # If no name provided, extract from URL
                    if not user_input[CONF_NAME]:
                        url_parts = user_input[CONF_STATION].rstrip("/").split("/")
                        user_input[CONF_NAME] = url_parts[-1].replace("-", " ").title()

                    # Create description with available gases
                    description = f"Available gases: {', '.join(available_gases)}" if available_gases else "No gases detected"
                    
                    # Store the URL in the correct format
                    entry_data = {
                        CONF_URL: user_input[CONF_STATION],
                        CONF_NAME: user_input[CONF_NAME],
                    }
                    
                    return self.async_create_entry(
                        title=f"Mosecom {user_input[CONF_NAME]}",
                        data=entry_data,
                        description=description,
                    )
                else:
                    errors[CONF_STATION] = "cannot_connect"

        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception: %s", err)
            errors["base"] = "unknown"

        # Rebuild form
        data_schema = self._build_form_schema()
        
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    def _build_form_schema(self) -> vol.Schema:
        """Build dynamic form schema based on available stations."""
        # Create station options - each station shows name, district, and address
        station_options = {}
        for station in self.stations:
            # Format: Name (District) - Address
            display_text = station['name']
            if station.get('district'):
                display_text += f" ({station['district']})"
            if station.get('address'):
                display_text += f" - {station['address']}"
            
            station_options[station["url"]] = display_text
        
        # Add default option if no stations selected
        if not station_options:
            station_options = {"": "No stations available - please try again later"}
        
        return vol.Schema(
            {
                vol.Required(CONF_STATION): vol.In(station_options),
                vol.Optional(CONF_NAME, default=""): str,
            }
        )
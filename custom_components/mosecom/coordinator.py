"""Data update coordinator for Moscow Air Quality Monitoring integration."""
from __future__ import annotations

import logging
import ssl
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import GAS_TYPES

_LOGGER = logging.getLogger(__name__)

# Create SSL context that doesn't verify certificates (for mosecom.mos.ru)
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class MosecomDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Moscow Air Quality data."""

    def __init__(self, hass, url: str):
        """Initialize."""
        self.url = url
        super().__init__(
            hass,
            _LOGGER,
            name="Moscow Air Quality",
            update_interval=timedelta(minutes=5),  # Update every 5 minutes
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(30):
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.url,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        },
                        ssl=SSL_CONTEXT,
                    ) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Error fetching data: {response.status}")
                        html_content = await response.text()

                        # Parse the HTML content
                        data = self._parse_html(html_content)
                        return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    def _parse_html(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content and extract air quality data."""
        import re

        data = {}

        # Find all data items in the entire document
        # Each gas appears twice: once for PDK (доли) and once for mg/m³
        item_pattern = r'<div class="text-norma">\s*([^<]+?)\s*</div>.*?<span class="this-count ">\s*([^<]+?)\s*</span>'
        items = re.findall(item_pattern, html_content, re.DOTALL)

        # Group values by gas type
        gas_values = {}
        for short_name, value in items:
            short_name = short_name.strip()
            value = value.strip().replace(',', '.')
            
            if short_name not in gas_values:
                gas_values[short_name] = []
            gas_values[short_name].append(value)

        # Process each gas - first value is PDK, second is mg/m³
        for gas_type, values in gas_values.items():
            if gas_type in GAS_TYPES and len(values) >= 2:
                try:
                    pdk_value = float(values[0])  # First occurrence is PDK
                    mg_m3_value = float(values[1])  # Second occurrence is mg/m³
                    
                    data[gas_type] = {
                        "name": GAS_TYPES[gas_type]["name"],
                        "name_ru": GAS_TYPES[gas_type]["name_ru"],
                        "mg_m3": mg_m3_value,
                        "pdk": pdk_value * 100,  # Convert to percentage
                    }
                    
                    _LOGGER.info(f"{gas_type}: PDK={pdk_value}, MG/M3={mg_m3_value}")
                except ValueError as e:
                    _LOGGER.warning(f"Could not parse values for {gas_type}: {values}, error: {e}")

        return data
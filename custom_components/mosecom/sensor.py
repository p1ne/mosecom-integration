"""Sensor platform for Moscow Air Quality Monitoring integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, GAS_TYPES, SENSOR_TYPE_MG_M3, SENSOR_TYPE_PDK
from .coordinator import MosecomDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Moscow Air Quality Monitoring sensors from a config entry."""
    coordinator: MosecomDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]
    location_name = entry.data.get(CONF_NAME, "Unknown")

    entities = []

    # Create sensors only for gases that are available at this station
    if coordinator.data:
        for gas_type, gas_data in coordinator.data.items():
            gas_info = GAS_TYPES.get(gas_type)
            if gas_info:
                # Create mg/m³ sensor
                entities.append(
                    MosecomSensor(
                        coordinator,
                        entry,
                        gas_type,
                        SENSOR_TYPE_MG_M3,
                        location_name,
                        gas_info["name"],
                        gas_info["unit_mg_m3"],
                    )
                )

                # Create PDK sensor
                entities.append(
                    MosecomSensor(
                        coordinator,
                        entry,
                        gas_type,
                        SENSOR_TYPE_PDK,
                        location_name,
                        gas_info["name"],
                        gas_info["unit_pdk"],
                    )
                )

    async_add_entities(entities)


class MosecomSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Moscow Air Quality Monitoring sensor."""

    def __init__(
        self,
        coordinator: MosecomDataUpdateCoordinator,
        entry: ConfigEntry,
        gas_type: str,
        sensor_type: str,
        location_name: str,
        gas_name: str,
        unit: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._gas_type = gas_type
        self._sensor_type = sensor_type
        self._location_name = location_name
        self._gas_name = gas_name
        self._unit = unit

        # Create unique ID with mosecom prefix, location, then gas type
        location_slug = location_name.lower().replace(" ", "_").replace("-", "_")
        self._attr_unique_id = f"mosecom_{location_slug}_{gas_type}_{sensor_type}"

        # Set device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"Mosecom {location_name}",
            "manufacturer": "Mosecom",
            "model": "Air Quality Monitor",
        }

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        if self._sensor_type == SENSOR_TYPE_MG_M3:
            return f"{self._location_name} {self._gas_type}"
        else:
            return f"{self._location_name} {self._gas_type} PDK"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self._gas_type in self.coordinator.data:
            gas_data = self.coordinator.data[self._gas_type]
            if self._sensor_type == SENSOR_TYPE_MG_M3:
                return gas_data["mg_m3"]
            else:
                return gas_data["pdk"]
        return None

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self._gas_type in self.coordinator.data
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if self.coordinator.data and self._gas_type in self.coordinator.data:
            gas_data = self.coordinator.data[self._gas_type]
            return {
                "gas_name_ru": gas_data["name_ru"],
                "gas_type": self._gas_type,
                "location": self._location_name,
            }
        return None
"""Test sensor."""

import logging

from pyrego600 import Register, RegoError, Type

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, timedelta
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RegoConfigEntry
from .entity import RegoEntity

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RegoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Test."""
    register = entry.runtime_data.heat_pump.last_error
    async_add_entities(
        [RegoLastErrorEntity(entry, register)],
        update_before_add=True,
    )

    async_add_entities(
        (
            RegoSensorEntity(entry, register)
            for register in entry.runtime_data.heat_pump.registers
            if register.type == Type.TEMPERATURE and not register.is_writtable
        ),
        update_before_add=True,
    )


class RegoSensorEntity(SensorEntity, RegoEntity):
    """An entity using CoordinatorEntity."""

    def __init__(self, entry: RegoConfigEntry, register: Register) -> None:
        """Test."""
        super().__init__(entry, register)

        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    async def async_update(self) -> None:
        """Boo."""
        try:
            self._attr_native_value = await self._heat_pump.read(self._register)
            self._attr_available = True
            self._attr_entity_registry_enabled_default = (
                self._attr_native_value is not None
            )
        except (OSError, RegoError) as e:
            self._attr_available = False
            _LOGGER.warning("Reading %s failed due %s", self._register.identifier, e)


class RegoLastErrorEntity(SensorEntity, RegoEntity):
    """An entity using CoordinatorEntity."""

    async def async_update(self) -> None:
        """Boo."""
        try:
            last_error = await self._heat_pump.read(self._register)
            self._attr_native_value = last_error.code
            self.extra_state_attributes = {"timestamp": last_error.timestamp}
            self._attr_available = True
        except (OSError, RegoError) as e:
            self._attr_available = False
            _LOGGER.warning("Reading %s failed due %s", self._register.identifier, e)

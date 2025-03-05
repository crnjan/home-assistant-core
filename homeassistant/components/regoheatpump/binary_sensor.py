"""bar."""

import logging

from pyrego600 import HeatPump, Register, RegoError, Type

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RegoConfigEntry

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RegoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Foo."""
    async_add_entities(
        (
            RegoEntity(entry, register)
            for register in entry.runtime_data.heat_pump.registers
            if register.type == Type.SWITCH and not register.is_writtable
        ),
        update_before_add=True,
    )


class RegoEntity(BinarySensorEntity):
    """An entity using CoordinatorEntity."""

    _heat_pump: HeatPump
    _register: Register

    _attr_has_entity_name = True

    def __init__(self, entry: RegoConfigEntry, register: Register) -> None:
        """Test."""
        super().__init__()

        self._heat_pump = entry.runtime_data.heat_pump
        self._register = register

        self._attr_unique_id = f"{entry.entry_id}.{register.identifier}"
        self._attr_device_info = entry.runtime_data.device_info
        # self._attr_translation_key = register.identifier
        self._attr_name = str(register.identifier)

    async def async_update(self) -> None:
        """Boo."""
        try:
            self.is_on = await self._heat_pump.read(self._register)
            self._attr_available = True
        except (OSError, RegoError) as e:
            self._attr_available = False
            _LOGGER.warning("Reading %s failed due %s", self._register.identifier, e)

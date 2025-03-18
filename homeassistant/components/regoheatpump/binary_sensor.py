"""bar."""

import logging

from pyrego600 import LastError, Type

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RegoConfigEntry
from .entity import RegoEntity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)
PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RegoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Foo."""
    async_add_entities(
        (
            RegoBinarySensorEntity(entry, register)
            for register in entry.runtime_data.heat_pump.registers
            if register.type == Type.SWITCH and not register.is_writtable
        ),
        update_before_add=True,
    )


class RegoBinarySensorEntity(BinarySensorEntity, RegoEntity):
    """An entity using CoordinatorEntity."""

    def process_value(self, value: int | LastError | None) -> None:
        """Test."""
        self.is_on = value != 0

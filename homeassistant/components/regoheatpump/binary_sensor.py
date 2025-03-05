"""bar."""

import logging

from pyrego600 import RegoError, Type

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import timedelta
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

    async def async_update(self) -> None:
        """Boo."""
        try:
            self.is_on = await self._heat_pump.read(self._register)
            self._attr_available = True
        except (OSError, RegoError) as e:
            self._attr_available = False
            _LOGGER.warning("Reading %s failed due %s", self._register.identifier, e)

"""Test sensor."""

from pyrego600 import HeatPump, Register

from homeassistant.components.sensor import Entity

from . import RegoConfigEntry


class RegoEntity(Entity):
    """An entity using CoordinatorEntity."""

    _heat_pump: HeatPump
    _register: Register

    _attr_has_entity_name = True

    def __init__(self, entry: RegoConfigEntry, register: Register) -> None:
        """Test."""
        super().__init__()

        self._heat_pump = entry.runtime_data.heat_pump
        self._register = register

        self._attr_unique_id = f"{entry.entry_id}-{register.identifier.group.value}-{register.identifier.id}"
        self._attr_device_info = entry.runtime_data.device_info
        self._attr_translation_key = (
            f"{register.identifier.group.value}-{register.identifier.id}"
        )
        # self._attr_name = f"{register.identifier.group.value}-{register.identifier.id}"

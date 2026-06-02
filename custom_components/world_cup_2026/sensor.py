from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])

    async_add_entities(
        [
            WorldCupFixturesSensor(api)
        ]
    )


class WorldCupFixturesSensor(SensorEntity):
    _attr_name = "World Cup Fixtures"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = "Ready"

    async def async_update(self):
        data = await self.api.get_matches()

        self._attr_extra_state_attributes = {
            "matches": data.get("matches", [])
        }

        self._attr_native_value = len(
            data.get("matches", [])
        )

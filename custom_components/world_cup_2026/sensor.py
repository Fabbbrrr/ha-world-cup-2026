from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])
    async_add_entities([WorldCupFixturesSensor(api)], True)


class WorldCupFixturesSensor(SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_2026_fixtures"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        simple_matches = []

        for m in matches[:40]:
            home = m.get("homeTeam", {})
            away = m.get("awayTeam", {})
            score = m.get("score", {}).get("fullTime", {})

            simple_matches.append({
                "utcDate": m.get("utcDate"),
                "status": m.get("status"),
                "stage": m.get("stage"),
                "group": m.get("group"),
                "home": home.get("shortName") or home.get("name"),
                "away": away.get("shortName") or away.get("name"),
                "homeScore": score.get("home"),
                "awayScore": score.get("away")
            })

        self._attr_extra_state_attributes = {
            "matches": simple_matches
        }

        self._attr_native_value = len(simple_matches)

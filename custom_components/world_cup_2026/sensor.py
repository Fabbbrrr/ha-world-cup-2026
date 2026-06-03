from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])

    async_add_entities([
        WorldCupFixturesSensor(api),
        WorldCupNextMatchSensor(api),
        WorldCupLiveMatchSensor(api),
    ], True)


class WorldCupFixturesSensor(SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_fixtures"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        self._attr_extra_state_attributes = {
            "matches": matches[:40]
        }

        self._attr_native_value = len(matches)


class WorldCupNextMatchSensor(SensorEntity):
    _attr_name = "World Cup Next Match"
    _attr_unique_id = "world_cup_next_match"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = "Unknown"

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        if matches:
            match = matches[0]

            home = match.get("home", "TBC")
            away = match.get("away", "TBC")

            self._attr_native_value = f"{home} v {away}"

            self._attr_extra_state_attributes = {
                "date": match.get("utcDate"),
                "status": match.get("status"),
                "group": match.get("group")
                class WorldCupLiveMatchesSensor(SensorEntity):
    _attr_name = "World Cup Live Matches"
    _attr_unique_id = "world_cup_live_matches"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        live = []

        for m in matches:
            if m.get("status") in ["IN_PLAY", "PAUSED"]:
                live.append({
                    "utcDate": m.get("utcDate"),
                    "status": m.get("status"),
                    "stage": m.get("stage"),
                    "group": m.get("group"),
                    "home": m.get("homeTeam", {}).get("shortName"),
                    "away": m.get("awayTeam", {}).get("shortName"),
                    "homeScore": m.get("score", {}).get("fullTime", {}).get("home"),
                    "awayScore": m.get("score", {}).get("fullTime", {}).get("away"),
                })

        self._attr_native_value = len(live)
        self._attr_extra_state_attributes = {
            "matches": live
        }
            }

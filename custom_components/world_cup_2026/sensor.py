from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])

    async_add_entities([
        WorldCupFixturesSensor(api),
        WorldCupNextMatchSensor(api),
        WorldCupLiveMatchesSensor(api),
    ], True)


class WorldCupFixturesSensor(SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_fixtures"

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
                "awayScore": score.get("away"),
            })

        self._attr_extra_state_attributes = {
            "matches": simple_matches
        }

        self._attr_native_value = len(simple_matches)


class WorldCupNextMatchSensor(SensorEntity):
    _attr_name = "World Cup Next Match"
    _attr_unique_id = "world_cup_next_match"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = "Unknown"
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        upcoming = [
            m for m in matches
            if m.get("status") in ["TIMED", "SCHEDULED"]
        ]

        if not upcoming:
            self._attr_native_value = "No upcoming matches"
            self._attr_extra_state_attributes = {}
            return

        match = upcoming[0]
        home = match.get("homeTeam", {}).get("shortName") or "TBD"
        away = match.get("awayTeam", {}).get("shortName") or "TBD"
        score = match.get("score", {}).get("fullTime", {})

        self._attr_native_value = f"{home} v {away}"

        self._attr_extra_state_attributes = {
            "utcDate": match.get("utcDate"),
            "status": match.get("status"),
            "stage": match.get("stage"),
            "group": match.get("group"),
            "home": home,
            "away": away,
            "homeScore": score.get("home"),
            "awayScore": score.get("away"),
        }


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
                home = m.get("homeTeam", {})
                away = m.get("awayTeam", {})
                score = m.get("score", {}).get("fullTime", {})

                live.append({
                    "utcDate": m.get("utcDate"),
                    "status": m.get("status"),
                    "stage": m.get("stage"),
                    "group": m.get("group"),
                    "home": home.get("shortName") or home.get("name"),
                    "away": away.get("shortName") or away.get("name"),
                    "homeScore": score.get("home"),
                    "awayScore": score.get("away"),
                })

        self._attr_native_value = len(live)
        self._attr_extra_state_attributes = {
            "matches": live
        }

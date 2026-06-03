from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])

    async_add_entities([
        WorldCupFixturesSensor(api),
        WorldCupNextMatchSensor(api),
        WorldCupLiveMatchesSensor(api),
        WorldCupTodayMatchesSensor(api),
    ], True)


def format_match(m):
    home = m.get("homeTeam", {})
    away = m.get("awayTeam", {})
    score = m.get("score", {}).get("fullTime", {})

    return {
        "utcDate": m.get("utcDate"),
        "status": m.get("status"),
        "stage": m.get("stage"),
        "group": m.get("group"),
        "home": home.get("shortName") or home.get("name") or "TBD",
        "away": away.get("shortName") or away.get("name") or "TBD",
        "homeScore": score.get("home"),
        "awayScore": score.get("away"),
    }


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

        self._attr_extra_state_attributes = {
            "matches": [format_match(m) for m in matches[:40]]
        }

        self._attr_native_value = len(matches)


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
        simple = format_match(match)

        self._attr_native_value = f"{simple['home']} v {simple['away']}"
        self._attr_extra_state_attributes = simple


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

        live = [
            format_match(m)
            for m in matches
            if m.get("status") in ["IN_PLAY", "PAUSED"]
        ]

        self._attr_native_value = len(live)
        self._attr_extra_state_attributes = {
            "matches": live
        }


class WorldCupTodayMatchesSensor(SensorEntity):
    _attr_name = "World Cup Today Matches"
    _attr_unique_id = "world_cup_today_matches"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        today = datetime.now(timezone.utc).date()

        todays_matches = []

        for m in matches:
            utc_date = m.get("utcDate")

            if not utc_date:
                continue

            try:
                match_date = datetime.fromisoformat(
                    utc_date.replace("Z", "+00:00")
                ).date()
            except ValueError:
                continue

            if match_date == today:
                todays_matches.append(format_match(m))

        self._attr_native_value = len(todays_matches)
        self._attr_extra_state_attributes = {
            "matches": todays_matches
        }

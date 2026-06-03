from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import SensorEntity

from .api import WorldCupAPI


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])

    sensors = [
        WorldCupFixturesSensor(api),
        WorldCupNextMatchSensor(api),
        WorldCupLiveMatchesSensor(api),
        WorldCupTodayMatchesSensor(api),
        WorldCupTomorrowMatchesSensor(api),
        WorldCupCompletedMatchesSensor(api),
        WorldCupTotalMatchesPlayedSensor(api),
        WorldCupTotalGoalsSensor(api),
        WorldCupTeamsRemainingSensor(api),
    ]

    for group in [
        "GROUP_A", "GROUP_B", "GROUP_C", "GROUP_D",
        "GROUP_E", "GROUP_F", "GROUP_G", "GROUP_H",
        "GROUP_I", "GROUP_J", "GROUP_K", "GROUP_L",
    ]:
        sensors.append(WorldCupGroupFixturesSensor(api, group))

    for stage in [
        "LAST_32",
        "LAST_16",
        "QUARTER_FINALS",
        "SEMI_FINALS",
        "THIRD_PLACE",
        "FINAL",
    ]:
        sensors.append(WorldCupStageFixturesSensor(api, stage))

    async_add_entities(sensors, True)


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


def parse_date(match):
    utc_date = match.get("utcDate")
    if not utc_date:
        return None

    try:
        return datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )
    except ValueError:
        return None


def clean_stage_name(stage):
    return stage.lower().replace("_", " ")


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

        self._attr_native_value = len(matches)
        self._attr_extra_state_attributes = {
            "matches": [format_match(m) for m in matches[:40]]
        }


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
        self._attr_extra_state_attributes = {"matches": live}


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

        filtered = [
            format_match(m)
            for m in matches
            if parse_date(m) and parse_date(m).date() == today
        ]

        self._attr_native_value = len(filtered)
        self._attr_extra_state_attributes = {"matches": filtered}


class WorldCupTomorrowMatchesSensor(SensorEntity):
    _attr_name = "World Cup Tomorrow Matches"
    _attr_unique_id = "world_cup_tomorrow_matches"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)

        filtered = [
            format_match(m)
            for m in matches
            if parse_date(m) and parse_date(m).date() == tomorrow
        ]

        self._attr_native_value = len(filtered)
        self._attr_extra_state_attributes = {"matches": filtered}


class WorldCupCompletedMatchesSensor(SensorEntity):
    _attr_name = "World Cup Completed Matches"
    _attr_unique_id = "world_cup_completed_matches"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        completed = [
            format_match(m)
            for m in matches
            if m.get("status") == "FINISHED"
        ]

        self._attr_native_value = len(completed)
        self._attr_extra_state_attributes = {
            "matches": completed[-20:]
        }


class WorldCupGroupFixturesSensor(SensorEntity):
    def __init__(self, api, group):
        self.api = api
        self.group = group
        group_name = group.replace("GROUP_", "Group ")
        self._attr_name = f"World Cup {group_name}"
        self._attr_unique_id = f"world_cup_{group.lower()}"
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        group_matches = [
            format_match(m)
            for m in matches
            if m.get("group") == self.group
        ]

        self._attr_native_value = len(group_matches)
        self._attr_extra_state_attributes = {
            "matches": group_matches
        }


class WorldCupStageFixturesSensor(SensorEntity):
    def __init__(self, api, stage):
        self.api = api
        self.stage = stage
        stage_name = clean_stage_name(stage).title()
        self._attr_name = f"World Cup {stage_name}"
        self._attr_unique_id = f"world_cup_{stage.lower()}"
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        stage_matches = [
            format_match(m)
            for m in matches
            if m.get("stage") == self.stage
        ]

        self._attr_native_value = len(stage_matches)
        self._attr_extra_state_attributes = {
            "matches": stage_matches
        }


class WorldCupTotalMatchesPlayedSensor(SensorEntity):
    _attr_name = "World Cup Total Matches Played"
    _attr_unique_id = "world_cup_total_matches_played"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        self._attr_native_value = len([
            m for m in matches
            if m.get("status") == "FINISHED"
        ])


class WorldCupTotalGoalsSensor(SensorEntity):
    _attr_name = "World Cup Total Goals"
    _attr_unique_id = "world_cup_total_goals"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 0

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        goals = 0

        for m in matches:
            if m.get("status") == "FINISHED":
                score = m.get("score", {}).get("fullTime", {})
                goals += score.get("home") or 0
                goals += score.get("away") or 0

        self._attr_native_value = goals


class WorldCupTeamsRemainingSensor(SensorEntity):
    _attr_name = "World Cup Teams Remaining"
    _attr_unique_id = "world_cup_teams_remaining"

    def __init__(self, api):
        self.api = api
        self._attr_native_value = 48

    async def async_update(self):
        data = await self.api.get_matches()
        matches = data.get("matches", [])

        final = [
            m for m in matches
            if m.get("stage") == "FINAL" and m.get("status") == "FINISHED"
        ]

        if final:
            self._attr_native_value = 1
        else:
            self._attr_native_value = 48

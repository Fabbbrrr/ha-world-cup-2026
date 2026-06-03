from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import WorldCupAPI
from .coordinator import WorldCupCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])
    coordinator = WorldCupCoordinator(hass, api)

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        WorldCupFixturesSensor(coordinator),
        WorldCupStandingsSensor(coordinator),
        WorldCupNextMatchSensor(coordinator),
        WorldCupLiveMatchesSensor(coordinator),
        WorldCupTodayMatchesSensor(coordinator),
        WorldCupTomorrowMatchesSensor(coordinator),
        WorldCupCompletedMatchesSensor(coordinator),
        WorldCupTotalMatchesPlayedSensor(coordinator),
        WorldCupTotalGoalsSensor(coordinator),
        WorldCupTeamsRemainingSensor(coordinator),
    ]

    for group in [
        "GROUP_A", "GROUP_B", "GROUP_C", "GROUP_D",
        "GROUP_E", "GROUP_F", "GROUP_G", "GROUP_H",
        "GROUP_I", "GROUP_J", "GROUP_K", "GROUP_L",
    ]:
        sensors.append(WorldCupGroupFixturesSensor(coordinator, group))

    for stage in [
        "LAST_32",
        "LAST_16",
        "QUARTER_FINALS",
        "SEMI_FINALS",
        "THIRD_PLACE",
        "FINAL",
    ]:
        sensors.append(WorldCupStageFixturesSensor(coordinator, stage))

    async_add_entities(sensors)


def get_matches(coordinator):
    return coordinator.data.get("matches", []) if coordinator.data else []


def get_standings(coordinator):
    return coordinator.data.get("standings", []) if coordinator.data else []


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
        return datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
    except ValueError:
        return None


def clean_stage_name(stage):
    return stage.lower().replace("_", " ")


class WorldCupFixturesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_fixtures"

    @property
    def native_value(self):
        return len(get_matches(self.coordinator))

    @property
    def extra_state_attributes(self):
        return {"matches": [format_match(m) for m in get_matches(self.coordinator)[:40]]}


class WorldCupStandingsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Standings"
    _attr_unique_id = "world_cup_standings"

    @property
    def native_value(self):
        return len(get_standings(self.coordinator))

    @property
    def extra_state_attributes(self):
        clean = []

        for group in get_standings(self.coordinator):
            table = []
            for team in group.get("table", []):
                team_data = team.get("team", {})
                table.append({
                    "position": team.get("position"),
                    "team": team_data.get("shortName") or team_data.get("name"),
                    "playedGames": team.get("playedGames"),
                    "won": team.get("won"),
                    "draw": team.get("draw"),
                    "lost": team.get("lost"),
                    "goalsFor": team.get("goalsFor"),
                    "goalsAgainst": team.get("goalsAgainst"),
                    "goalDifference": team.get("goalDifference"),
                    "points": team.get("points"),
                })

            clean.append({
                "group": group.get("group"),
                "stage": group.get("stage"),
                "table": table,
            })

        return {"standings": clean}


class WorldCupNextMatchSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Next Match"
    _attr_unique_id = "world_cup_next_match"

    @property
    def native_value(self):
        upcoming = [m for m in get_matches(self.coordinator) if m.get("status") in ["TIMED", "SCHEDULED"]]
        if not upcoming:
            return "No upcoming matches"
        m = format_match(upcoming[0])
        return f"{m['home']} v {m['away']}"

    @property
    def extra_state_attributes(self):
        upcoming = [m for m in get_matches(self.coordinator) if m.get("status") in ["TIMED", "SCHEDULED"]]
        return format_match(upcoming[0]) if upcoming else {}


class WorldCupLiveMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Live Matches"
    _attr_unique_id = "world_cup_live_matches"

    @property
    def native_value(self):
        return len([m for m in get_matches(self.coordinator) if m.get("status") in ["IN_PLAY", "PAUSED"]])

    @property
    def extra_state_attributes(self):
        return {
            "matches": [
                format_match(m)
                for m in get_matches(self.coordinator)
                if m.get("status") in ["IN_PLAY", "PAUSED"]
            ]
        }


class WorldCupTodayMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Today Matches"
    _attr_unique_id = "world_cup_today_matches"

    @property
    def native_value(self):
        return len(self.extra_state_attributes["matches"])

    @property
    def extra_state_attributes(self):
        today = datetime.now(timezone.utc).date()
        return {
            "matches": [
                format_match(m)
                for m in get_matches(self.coordinator)
                if parse_date(m) and parse_date(m).date() == today
            ]
        }


class WorldCupTomorrowMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Tomorrow Matches"
    _attr_unique_id = "world_cup_tomorrow_matches"

    @property
    def native_value(self):
        return len(self.extra_state_attributes["matches"])

    @property
    def extra_state_attributes(self):
        tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)
        return {
            "matches": [
                format_match(m)
                for m in get_matches(self.coordinator)
                if parse_date(m) and parse_date(m).date() == tomorrow
            ]
        }


class WorldCupCompletedMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Completed Matches"
    _attr_unique_id = "world_cup_completed_matches"

    @property
    def native_value(self):
        return len([m for m in get_matches(self.coordinator) if m.get("status") == "FINISHED"])

    @property
    def extra_state_attributes(self):
        completed = [
            format_match(m)
            for m in get_matches(self.coordinator)
            if m.get("status") == "FINISHED"
        ]
        return {"matches": completed[-20:]}


class WorldCupGroupFixturesSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, group):
        super().__init__(coordinator)
        self.group = group
        group_name = group.replace("GROUP_", "Group ")
        self._attr_name = f"World Cup {group_name}"
        self._attr_unique_id = f"world_cup_{group.lower()}"

    @property
    def native_value(self):
        return len(self.extra_state_attributes["matches"])

    @property
    def extra_state_attributes(self):
        return {
            "matches": [
                format_match(m)
                for m in get_matches(self.coordinator)
                if m.get("group") == self.group
            ]
        }


class WorldCupStageFixturesSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, stage):
        super().__init__(coordinator)
        self.stage = stage
        self._attr_name = f"World Cup {clean_stage_name(stage).title()}"
        self._attr_unique_id = f"world_cup_{stage.lower()}"

    @property
    def native_value(self):
        return len(self.extra_state_attributes["matches"])

    @property
    def extra_state_attributes(self):
        return {
            "matches": [
                format_match(m)
                for m in get_matches(self.coordinator)
                if m.get("stage") == self.stage
            ]
        }


class WorldCupTotalMatchesPlayedSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Total Matches Played"
    _attr_unique_id = "world_cup_total_matches_played"

    @property
    def native_value(self):
        return len([m for m in get_matches(self.coordinator) if m.get("status") == "FINISHED"])


class WorldCupTotalGoalsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Total Goals"
    _attr_unique_id = "world_cup_total_goals"

    @property
    def native_value(self):
        goals = 0
        for m in get_matches(self.coordinator):
            if m.get("status") == "FINISHED":
                score = m.get("score", {}).get("fullTime", {})
                goals += score.get("home") or 0
                goals += score.get("away") or 0
        return goals


class WorldCupTeamsRemainingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Teams Remaining"
    _attr_unique_id = "world_cup_teams_remaining"

    @property
    def native_value(self):
        final_finished = [
            m for m in get_matches(self.coordinator)
            if m.get("stage") == "FINAL" and m.get("status") == "FINISHED"
        ]
        return 1 if final_finished else 48

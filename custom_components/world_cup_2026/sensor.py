from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import WorldCupAPI
from .coordinator import WorldCupCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    api = WorldCupAPI(entry.data["api_key"])
    coordinator = WorldCupCoordinator(hass, api)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        WorldCupFixturesSensor(coordinator),
        WorldCupStandingsSensor(coordinator),
        WorldCupNextMatchSensor(coordinator),
        WorldCupLiveMatchesSensor(coordinator),
    ])


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


class WorldCupFixturesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_fixtures"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("matches", []))

    @property
    def extra_state_attributes(self):
        matches = self.coordinator.data.get("matches", [])
        return {
            "matches": [format_match(m) for m in matches[:40]]
        }


class WorldCupStandingsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Standings"
    _attr_unique_id = "world_cup_standings"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("standings", []))

    @property
    def extra_state_attributes(self):
        standings = self.coordinator.data.get("standings", [])
        clean = []

        for group in standings:
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

        return {
            "standings": clean
        }


class WorldCupNextMatchSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Next Match"
    _attr_unique_id = "world_cup_next_match"

    @property
    def native_value(self):
        matches = self.coordinator.data.get("matches", [])

        upcoming = [
            m for m in matches
            if m.get("status") in ["TIMED", "SCHEDULED"]
        ]

        if not upcoming:
            return "No upcoming matches"

        match = format_match(upcoming[0])
        return f"{match['home']} v {match['away']}"

    @property
    def extra_state_attributes(self):
        matches = self.coordinator.data.get("matches", [])

        upcoming = [
            m for m in matches
            if m.get("status") in ["TIMED", "SCHEDULED"]
        ]

        if not upcoming:
            return {}

        return format_match(upcoming[0])


class WorldCupLiveMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Live Matches"
    _attr_unique_id = "world_cup_live_matches"

    @property
    def native_value(self):
        matches = self.coordinator.data.get("matches", [])

        live = [
            m for m in matches
            if m.get("status") in ["IN_PLAY", "PAUSED"]
        ]

        return len(live)

    @property
    def extra_state_attributes(self):
        matches = self.coordinator.data.get("matches", [])

        live = [
            format_match(m)
            for m in matches
            if m.get("status") in ["IN_PLAY", "PAUSED"]
        ]

        return {
            "matches": live
        }

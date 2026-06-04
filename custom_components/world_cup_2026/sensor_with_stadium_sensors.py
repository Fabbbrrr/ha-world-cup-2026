from datetime import datetime, timezone, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import WorldCupAPI
from .coordinator import WorldCupCoordinator


TOTAL_WORLD_CUP_MATCHES = 104
TOTAL_WORLD_CUP_TEAMS = 48


WORLD_CUP_STADIUMS = [
    {
        "stadium": "MetLife Stadium",
        "city": "New York/New Jersey",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 82500,
        "note": "Final venue",
    },
    {
        "stadium": "AT&T Stadium",
        "city": "Dallas",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 80000,
        "note": "Host venue",
    },
    {
        "stadium": "SoFi Stadium",
        "city": "Los Angeles",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 70000,
        "note": "Host venue",
    },
    {
        "stadium": "Mercedes-Benz Stadium",
        "city": "Atlanta",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 71000,
        "note": "Host venue",
    },
    {
        "stadium": "Lincoln Financial Field",
        "city": "Philadelphia",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 69000,
        "note": "Host venue",
    },
    {
        "stadium": "NRG Stadium",
        "city": "Houston",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 72000,
        "note": "Host venue",
    },
    {
        "stadium": "Hard Rock Stadium",
        "city": "Miami",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 65000,
        "note": "Host venue",
    },
    {
        "stadium": "Lumen Field",
        "city": "Seattle",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 69000,
        "note": "Host venue",
    },
    {
        "stadium": "Levi's Stadium",
        "city": "San Francisco Bay Area",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 68000,
        "note": "Host venue",
    },
    {
        "stadium": "GEHA Field at Arrowhead Stadium",
        "city": "Kansas City",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 76000,
        "note": "Host venue",
    },
    {
        "stadium": "Gillette Stadium",
        "city": "Boston",
        "country": "USA",
        "flag": "🇺🇸",
        "capacity": 65000,
        "note": "Host venue",
    },
    {
        "stadium": "BC Place",
        "city": "Vancouver",
        "country": "Canada",
        "flag": "🇨🇦",
        "capacity": 54500,
        "note": "Host venue",
    },
    {
        "stadium": "BMO Field",
        "city": "Toronto",
        "country": "Canada",
        "flag": "🇨🇦",
        "capacity": 45000,
        "note": "Host venue",
    },
    {
        "stadium": "Estadio Azteca",
        "city": "Mexico City",
        "country": "Mexico",
        "flag": "🇲🇽",
        "capacity": 87000,
        "note": "Opening match venue",
    },
    {
        "stadium": "Estadio BBVA",
        "city": "Monterrey",
        "country": "Mexico",
        "flag": "🇲🇽",
        "capacity": 53500,
        "note": "Host venue",
    },
    {
        "stadium": "Estadio Akron",
        "city": "Guadalajara",
        "country": "Mexico",
        "flag": "🇲🇽",
        "capacity": 48000,
        "note": "Host venue",
    },
]


def get_stadiums():
    return WORLD_CUP_STADIUMS


def get_host_cities():
    return [
        {
            "city": venue["city"],
            "country": venue["country"],
            "flag": venue["flag"],
            "stadium": venue["stadium"],
        }
        for venue in WORLD_CUP_STADIUMS
    ]


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
        WorldCupMatchesRemainingSensor(coordinator),
        WorldCupProgressSensor(coordinator),
        WorldCupTotalGoalsSensor(coordinator),
        WorldCupGoalsPerMatchSensor(coordinator),
        WorldCupTeamsRemainingSensor(coordinator),
        WorldCupCurrentStageSensor(coordinator),

        WorldCupTopScorersSensor(coordinator),
        WorldCupTopScorerSensor(coordinator),
        WorldCupTopAssistsSensor(coordinator),
        WorldCupTopAssistSensor(coordinator),

        WorldCupBiggestWinSensor(coordinator),
        WorldCupHighestScoringMatchSensor(coordinator),
        WorldCupLatestResultSensor(coordinator),
        WorldCupTopScoringTeamSensor(coordinator),
        WorldCupBestDefenceSensor(coordinator),
        WorldCupEliminatedTeamsSensor(coordinator),
        WorldCupLiveGoalsSensor(coordinator),

        WorldCupCountdownSensor(coordinator),
        WorldCupDaysUntilFinalSensor(coordinator),

        WorldCupStadiumsSensor(coordinator),
        WorldCupHostCitiesSensor(coordinator),
        WorldCupFinalVenueSensor(coordinator),
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


def get_scorers(coordinator):
    return coordinator.data.get("scorers", []) if coordinator.data else []


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


def format_scorer(s):
    player = s.get("player", {})
    team = s.get("team", {})

    return {
        "name": player.get("name") or "Unknown",
        "firstName": player.get("firstName"),
        "lastName": player.get("lastName"),
        "dateOfBirth": player.get("dateOfBirth"),
        "nationality": player.get("nationality"),
        "team": team.get("shortName") or team.get("name") or "Unknown",
        "goals": s.get("goals") or 0,
        "assists": s.get("assists") or 0,
        "penalties": s.get("penalties") or 0,
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


def pretty_stage(stage):
    if not stage:
        return "Not started"

    names = {
        "GROUP_STAGE": "Group Stage",
        "LAST_32": "Last 32",
        "LAST_16": "Last 16",
        "QUARTER_FINALS": "Quarter Finals",
        "SEMI_FINALS": "Semi Finals",
        "THIRD_PLACE": "Third Place",
        "FINAL": "Final",
    }
    return names.get(stage, clean_stage_name(stage).title())


def finished_matches(coordinator):
    return [
        m for m in get_matches(coordinator)
        if m.get("status") == "FINISHED"
    ]


def live_matches(coordinator):
    return [
        m for m in get_matches(coordinator)
        if m.get("status") in ["IN_PLAY", "PAUSED"]
    ]


def full_time_score(match):
    score = match.get("score", {}).get("fullTime", {})
    home = score.get("home")
    away = score.get("away")
    return home, away


def team_name(team):
    return team.get("shortName") or team.get("name") or "Unknown"


def get_home_away_names(match):
    return team_name(match.get("homeTeam", {})), team_name(match.get("awayTeam", {}))


def get_team_goal_stats(coordinator):
    stats = {}

    for match in finished_matches(coordinator):
        home, away = get_home_away_names(match)
        home_score, away_score = full_time_score(match)

        if home_score is None or away_score is None:
            continue

        for name in [home, away]:
            if name not in stats:
                stats[name] = {
                    "team": name,
                    "goalsFor": 0,
                    "goalsAgainst": 0,
                    "goalDifference": 0,
                    "played": 0,
                }

        stats[home]["goalsFor"] += home_score
        stats[home]["goalsAgainst"] += away_score
        stats[home]["played"] += 1

        stats[away]["goalsFor"] += away_score
        stats[away]["goalsAgainst"] += home_score
        stats[away]["played"] += 1

    for item in stats.values():
        item["goalDifference"] = item["goalsFor"] - item["goalsAgainst"]

    return list(stats.values())


class WorldCupFixturesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Fixtures"
    _attr_unique_id = "world_cup_fixtures"

    @property
    def native_value(self):
        return len(get_matches(self.coordinator))

    @property
    def extra_state_attributes(self):
        # Keep attributes limited so Home Assistant does not overload the state machine.
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
        upcoming = [
            m for m in get_matches(self.coordinator)
            if m.get("status") in ["TIMED", "SCHEDULED"]
        ]
        if not upcoming:
            return "No upcoming matches"
        m = format_match(upcoming[0])
        return f"{m['home']} v {m['away']}"

    @property
    def extra_state_attributes(self):
        upcoming = [
            m for m in get_matches(self.coordinator)
            if m.get("status") in ["TIMED", "SCHEDULED"]
        ]
        return format_match(upcoming[0]) if upcoming else {}


class WorldCupLiveMatchesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Live Matches"
    _attr_unique_id = "world_cup_live_matches"

    @property
    def native_value(self):
        return len(live_matches(self.coordinator))

    @property
    def extra_state_attributes(self):
        return {
            "matches": [
                format_match(m)
                for m in live_matches(self.coordinator)
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
        return len(finished_matches(self.coordinator))

    @property
    def extra_state_attributes(self):
        completed = [
            format_match(m)
            for m in finished_matches(self.coordinator)
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
        return len(finished_matches(self.coordinator))


class WorldCupMatchesRemainingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Matches Remaining"
    _attr_unique_id = "world_cup_matches_remaining"

    @property
    def native_value(self):
        played = len(finished_matches(self.coordinator))
        return max(TOTAL_WORLD_CUP_MATCHES - played, 0)


class WorldCupProgressSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Progress"
    _attr_unique_id = "world_cup_progress"
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        played = len(finished_matches(self.coordinator))
        return round((played / TOTAL_WORLD_CUP_MATCHES) * 100, 1)


class WorldCupTotalGoalsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Total Goals"
    _attr_unique_id = "world_cup_total_goals"

    @property
    def native_value(self):
        goals = 0
        for m in finished_matches(self.coordinator):
            home, away = full_time_score(m)
            goals += home or 0
            goals += away or 0
        return goals


class WorldCupGoalsPerMatchSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Goals Per Match"
    _attr_unique_id = "world_cup_goals_per_match"

    @property
    def native_value(self):
        played = len(finished_matches(self.coordinator))
        if played == 0:
            return 0

        goals = 0
        for m in finished_matches(self.coordinator):
            home, away = full_time_score(m)
            goals += home or 0
            goals += away or 0

        return round(goals / played, 2)


class WorldCupTeamsRemainingSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Teams Remaining"
    _attr_unique_id = "world_cup_teams_remaining"

    @property
    def native_value(self):
        stages = [m.get("stage") for m in get_matches(self.coordinator) if m.get("stage")]

        if any(m.get("stage") == "FINAL" and m.get("status") == "FINISHED" for m in get_matches(self.coordinator)):
            return 1
        if "FINAL" in stages:
            return 2
        if "SEMI_FINALS" in stages:
            return 4
        if "QUARTER_FINALS" in stages:
            return 8
        if "LAST_16" in stages:
            return 16
        if "LAST_32" in stages:
            return 32

        return TOTAL_WORLD_CUP_TEAMS


class WorldCupCurrentStageSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Current Stage"
    _attr_unique_id = "world_cup_current_stage"

    @property
    def native_value(self):
        live = live_matches(self.coordinator)
        if live:
            stages = [m.get("stage") for m in live if m.get("stage")]
            if stages:
                return pretty_stage(stages[0])

        unfinished = [
            m for m in get_matches(self.coordinator)
            if m.get("status") in ["TIMED", "SCHEDULED", "IN_PLAY", "PAUSED"]
        ]
        if unfinished:
            stage = unfinished[0].get("stage")
            return pretty_stage(stage)

        finished = finished_matches(self.coordinator)
        if finished:
            stage = finished[-1].get("stage")
            return pretty_stage(stage)

        return "Not started"


class WorldCupTopScorersSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Top Scorers"
    _attr_unique_id = "world_cup_top_scorers"

    @property
    def native_value(self):
        return len(get_scorers(self.coordinator))

    @property
    def extra_state_attributes(self):
        scorers = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
        ]
        scorers.sort(key=lambda x: x.get("goals", 0), reverse=True)
        return {"scorers": scorers[:20]}


class WorldCupTopScorerSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Top Scorer"
    _attr_unique_id = "world_cup_top_scorer"

    @property
    def native_value(self):
        scorers = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
        ]
        scorers.sort(key=lambda x: x.get("goals", 0), reverse=True)

        if not scorers:
            return "No scorers yet"

        top = scorers[0]
        return f"{top['name']} - {top['goals']} goals"

    @property
    def extra_state_attributes(self):
        scorers = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
        ]
        scorers.sort(key=lambda x: x.get("goals", 0), reverse=True)
        return scorers[0] if scorers else {}


class WorldCupTopAssistsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Top Assists"
    _attr_unique_id = "world_cup_top_assists"

    @property
    def native_value(self):
        assists = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
            if (s.get("assists") or 0) > 0
        ]
        return len(assists)

    @property
    def extra_state_attributes(self):
        assists = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
            if (s.get("assists") or 0) > 0
        ]
        assists.sort(key=lambda x: x.get("assists", 0), reverse=True)
        return {"assists": assists[:20]}


class WorldCupTopAssistSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Top Assist"
    _attr_unique_id = "world_cup_top_assist"

    @property
    def native_value(self):
        assists = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
            if (s.get("assists") or 0) > 0
        ]
        assists.sort(key=lambda x: x.get("assists", 0), reverse=True)

        if not assists:
            return "No assists yet"

        top = assists[0]
        return f"{top['name']} - {top['assists']} assists"

    @property
    def extra_state_attributes(self):
        assists = [
            format_scorer(s)
            for s in get_scorers(self.coordinator)
            if (s.get("assists") or 0) > 0
        ]
        assists.sort(key=lambda x: x.get("assists", 0), reverse=True)
        return assists[0] if assists else {}


class WorldCupBiggestWinSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Biggest Win"
    _attr_unique_id = "world_cup_biggest_win"

    @property
    def native_value(self):
        biggest = None

        for m in finished_matches(self.coordinator):
            home_score, away_score = full_time_score(m)
            if home_score is None or away_score is None:
                continue

            margin = abs(home_score - away_score)
            if margin == 0:
                continue

            if biggest is None or margin > biggest["margin"]:
                home, away = get_home_away_names(m)
                biggest = {
                    "home": home,
                    "away": away,
                    "homeScore": home_score,
                    "awayScore": away_score,
                    "margin": margin,
                }

        if not biggest:
            return "No result yet"

        return f"{biggest['home']} {biggest['homeScore']}-{biggest['awayScore']} {biggest['away']}"

    @property
    def extra_state_attributes(self):
        biggest = None

        for m in finished_matches(self.coordinator):
            home_score, away_score = full_time_score(m)
            if home_score is None or away_score is None:
                continue

            margin = abs(home_score - away_score)
            if margin == 0:
                continue

            if biggest is None or margin > biggest["margin"]:
                home, away = get_home_away_names(m)
                biggest = {
                    "home": home,
                    "away": away,
                    "homeScore": home_score,
                    "awayScore": away_score,
                    "margin": margin,
                    "utcDate": m.get("utcDate"),
                    "stage": m.get("stage"),
                    "group": m.get("group"),
                }

        return biggest or {}


class WorldCupHighestScoringMatchSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Highest Scoring Match"
    _attr_unique_id = "world_cup_highest_scoring_match"

    @property
    def native_value(self):
        highest = None

        for m in finished_matches(self.coordinator):
            home_score, away_score = full_time_score(m)
            if home_score is None or away_score is None:
                continue

            total_goals = home_score + away_score

            if highest is None or total_goals > highest["totalGoals"]:
                home, away = get_home_away_names(m)
                highest = {
                    "home": home,
                    "away": away,
                    "homeScore": home_score,
                    "awayScore": away_score,
                    "totalGoals": total_goals,
                }

        if not highest:
            return "No result yet"

        return f"{highest['home']} {highest['homeScore']}-{highest['awayScore']} {highest['away']}"

    @property
    def extra_state_attributes(self):
        highest = None

        for m in finished_matches(self.coordinator):
            home_score, away_score = full_time_score(m)
            if home_score is None or away_score is None:
                continue

            total_goals = home_score + away_score

            if highest is None or total_goals > highest["totalGoals"]:
                home, away = get_home_away_names(m)
                highest = {
                    "home": home,
                    "away": away,
                    "homeScore": home_score,
                    "awayScore": away_score,
                    "totalGoals": total_goals,
                    "utcDate": m.get("utcDate"),
                    "stage": m.get("stage"),
                    "group": m.get("group"),
                }

        return highest or {}


class WorldCupLatestResultSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Latest Result"
    _attr_unique_id = "world_cup_latest_result"

    @property
    def native_value(self):
        matches = finished_matches(self.coordinator)
        if not matches:
            return "No result yet"

        latest = sorted(
            matches,
            key=lambda m: parse_date(m) or datetime.min.replace(tzinfo=timezone.utc),
        )[-1]

        home, away = get_home_away_names(latest)
        home_score, away_score = full_time_score(latest)
        return f"{home} {home_score}-{away_score} {away}"

    @property
    def extra_state_attributes(self):
        matches = finished_matches(self.coordinator)
        if not matches:
            return {}

        latest = sorted(
            matches,
            key=lambda m: parse_date(m) or datetime.min.replace(tzinfo=timezone.utc),
        )[-1]

        return format_match(latest)


class WorldCupTopScoringTeamSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Top Scoring Team"
    _attr_unique_id = "world_cup_top_scoring_team"

    @property
    def native_value(self):
        stats = get_team_goal_stats(self.coordinator)
        if not stats:
            return "No goals yet"

        stats.sort(key=lambda x: x["goalsFor"], reverse=True)
        top = stats[0]
        return f"{top['team']} - {top['goalsFor']} goals"

    @property
    def extra_state_attributes(self):
        stats = get_team_goal_stats(self.coordinator)
        stats.sort(key=lambda x: x["goalsFor"], reverse=True)
        return {"teams": stats[:20]}


class WorldCupBestDefenceSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Best Defence"
    _attr_unique_id = "world_cup_best_defence"

    @property
    def native_value(self):
        stats = [s for s in get_team_goal_stats(self.coordinator) if s["played"] > 0]
        if not stats:
            return "No data yet"

        stats.sort(key=lambda x: (x["goalsAgainst"], -x["played"]))
        top = stats[0]
        return f"{top['team']} - {top['goalsAgainst']} conceded"

    @property
    def extra_state_attributes(self):
        stats = [s for s in get_team_goal_stats(self.coordinator) if s["played"] > 0]
        stats.sort(key=lambda x: (x["goalsAgainst"], -x["played"]))
        return {"teams": stats[:20]}


class WorldCupEliminatedTeamsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Eliminated Teams"
    _attr_unique_id = "world_cup_eliminated_teams"

    @property
    def native_value(self):
        remaining = WorldCupTeamsRemainingSensor(self.coordinator).native_value
        if isinstance(remaining, int):
            return max(TOTAL_WORLD_CUP_TEAMS - remaining, 0)
        return 0


class WorldCupLiveGoalsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Live Goals"
    _attr_unique_id = "world_cup_live_goals"

    @property
    def native_value(self):
        goals = 0

        for m in live_matches(self.coordinator):
            home_score, away_score = full_time_score(m)
            goals += home_score or 0
            goals += away_score or 0

        return goals

    @property
    def extra_state_attributes(self):
        return {
            "matches": [
                format_match(m)
                for m in live_matches(self.coordinator)
            ]
        }


class WorldCupCountdownSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Countdown"
    _attr_unique_id = "world_cup_countdown"
    _attr_native_unit_of_measurement = "days"

    @property
    def native_value(self):
        kickoff = datetime(2026, 6, 11, 20, 0, 0, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days = (kickoff - now).days
        return max(days, 0)


class WorldCupDaysUntilFinalSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Days Until Final"
    _attr_unique_id = "world_cup_days_until_final"
    _attr_native_unit_of_measurement = "days"

    @property
    def native_value(self):
        final_date = datetime(2026, 7, 19, 20, 0, 0, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days = (final_date - now).days
        return max(days, 0)

class WorldCupStadiumsSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Stadiums"
    _attr_unique_id = "world_cup_stadiums"

    @property
    def native_value(self):
        return len(get_stadiums())

    @property
    def extra_state_attributes(self):
        return {
            "stadiums": get_stadiums(),
            "usa_stadiums": [
                venue for venue in get_stadiums()
                if venue.get("country") == "USA"
            ],
            "canada_stadiums": [
                venue for venue in get_stadiums()
                if venue.get("country") == "Canada"
            ],
            "mexico_stadiums": [
                venue for venue in get_stadiums()
                if venue.get("country") == "Mexico"
            ],
        }


class WorldCupHostCitiesSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Host Cities"
    _attr_unique_id = "world_cup_host_cities"

    @property
    def native_value(self):
        return len(get_host_cities())

    @property
    def extra_state_attributes(self):
        return {"cities": get_host_cities()}


class WorldCupFinalVenueSensor(CoordinatorEntity, SensorEntity):
    _attr_name = "World Cup Final Venue"
    _attr_unique_id = "world_cup_final_venue"

    @property
    def native_value(self):
        final_venue = next(
            (venue for venue in get_stadiums() if venue.get("stadium") == "MetLife Stadium"),
            None,
        )

        if not final_venue:
            return "Unknown"

        return f"{final_venue['stadium']} - {final_venue['city']}"

    @property
    def extra_state_attributes(self):
        final_venue = next(
            (venue for venue in get_stadiums() if venue.get("stadium") == "MetLife Stadium"),
            None,
        )

        return final_venue or {}

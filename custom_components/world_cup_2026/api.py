"""World Cup API."""

import aiohttp


class WorldCupAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_matches(self):
        headers = {"X-Auth-Token": self.api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.football-data.org/v4/competitions/WC/matches",
                headers=headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_standings(self):
        headers = {"X-Auth-Token": self.api_key}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.football-data.org/v4/competitions/WC/standings",
                headers=headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

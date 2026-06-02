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
                return await response.json()

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WorldCupAPI

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)


class WorldCupCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api: WorldCupAPI):
        super().__init__(
            hass,
            _LOGGER,
            name="World Cup 2026",
            update_interval=SCAN_INTERVAL,
        )
        self.api = api

    async def _async_update_data(self):
        try:
            matches = await self.api.get_matches()
            standings = await self.api.get_standings()

            return {
                "matches": matches.get("matches", []),
                "standings": standings.get("standings", []),
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching World Cup data: {err}") from err

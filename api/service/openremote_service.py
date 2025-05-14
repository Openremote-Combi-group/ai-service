from openremote_client import OpenRemoteClient
from openremote_client.schemas import asset_object
from api import config


class OpenRemoteService:
    client: OpenRemoteClient

    def __init__(self):
        self.client = OpenRemoteClient(
            host=config.openremote_host,
            client_id=config.openremote_client_id,
            client_secret=config.openremote_client_secret,
        )

    async def fetch_all_assets(self) -> list[asset_object]:
        assets = await self.client.asset.query({})

        return assets

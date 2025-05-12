from datetime import datetime, timedelta
import json
from typing import Literal

import httpx
from pydantic import HttpUrl

from api.config import config


class OpenRemoteService:
    access_token: str | None = None
    expires_on: datetime | None = None

    def __init__(self):
        self.cookie = None

    async def fetch_openapi_specs(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.build_url("/openapi.json"))

            response.raise_for_status()

            json_content = response.json()

            return json.dumps(json_content['paths'], indent=1)

    async def _authenticate(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.build_url("/auth/realms/master/protocol/openid-connect/token", base_url_only=True),
                data={
                    "grant_type": "client_credentials",
                    "client_id": config.openremote_client_id,
                    "client_secret": config.openremote_client_secret,
                    "scope": "profile"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()

            json = response.json()

            self.access_token = json["access_token"]
            self.expires_on = datetime.now() + timedelta(seconds=json["expires_in"] - 1)
            
    def is_authenticated(self) -> bool:
        if self.access_token is None or (self.expires_on and datetime.now() >= self.expires_on):
            return False
        return True

    async def get_auth_token(self) -> str:
        if not self.is_authenticated():
            await self._authenticate()
        return self.access_token

    def build_url(self, path: str, base_url_only: bool = False) -> str:
        if path.startswith('/'):
            path = path[1:]
        if base_url_only:
            return str(config.openremote_host) + path

        return str(config.openremote_host) + "api/master/" + path

    async def send_request(self, method: Literal['GET', 'POST'], path: str, params: dict | None = None, headers: dict | None = None, content: str | None = None):
        """
        Retrieves data from the given remote path using an asynchronous HTTP GET
        request. This function creates an asynchronous HTTP client, sends a GET
        request to the specified path, and processes the response.
        The Authentication token is handled automatically.
        The Content-Type is set to application/json automatically.

        :param method: The method to use for the request
        :type method: str

        :param path: The remote path to which the request is sent. The full URL (host & /api/master) is automatically provided so only include the path of the endpoint.
        :type path: str

        :param params: Optional query parameters to include in the request.
        :type params: dict or None

        :param headers: Optional HTTP headers to include in the request.
        :type headers: dict or None

        :param content: Optional content/body to send with the POST request.
        :type content: str or None

        :return: The response from the remote server.
        :rtype: Any
        """
        if headers is None:
            headers = {}

        headers['accept'] = "application/json"
        headers['Authorization'] = f"Bearer {await self.get_auth_token()}"

        async with httpx.AsyncClient() as client:
            print("CONTENT URL SEND")
            print(self.build_url(path))

            return await client.request(
                method=method,
                url=self.build_url(path),
                params=params,
                headers=headers,
                content=content
            )


    async def post(self, path: str, params: dict | None = None, headers: dict | None = None, content: str | None = None):
        """
        Sends data to the given remote path using an asynchronous HTTP POST
        request. This function creates an asynchronous HTTP client, sends a POST
        request to the specified path, and processes the response.
        The Authentication token is handled automatically.
        The Content-Type is set to application/json automatically.

        :param path: The remote path to which the POST request is sent. The full URL (host & /api/master) is automatically provided so only include the path of the endpoint.
        :type path: str
        :param params: Optional query parameters to include in the request.
        :type params: dict or None
        :param headers: Optional HTTP headers to include in the request.
        :type headers: dict or None
        :param content: Optional content/body to send with the POST request.
        :type content: str or None

        :return: The response from the remote server.
        :rtype: Any
        """
        if headers is None:
            headers = {}

        headers['accept'] = "application/json"
        headers['Authorization'] = f"Bearer {await self.get_auth_token()}"

        async with httpx.AsyncClient() as client:
            return await client.post(
                self.build_url(path),
                params=params,
                headers=headers,
                content=content
            )

    def fetch_assets(self):
        return json.loads("""
    [{
  "id": "71F157uBwTR2WI9xMB7PwX",
  "version": 4,
  "createdOn": 1744878843597,
  "name": "Fontys R10",
  "accessPublicRead": false,
  "parentId": "56SzD7ckLvgQe8WAXDe5uE",
  "realm": "master",
  "type": "BuildingAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE",
    "71F157uBwTR2WI9xMB7PwX"
  ],
  "attributes": {
    "area": {
      "name": "area",
      "type": "positiveInteger",
      "meta": {
        "ruleState": true
      },
      "value": 20,
      "timestamp": 1744879288866
    },
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": "Netherlands",
      "timestamp": 1744879240113
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "city": {
      "name": "city",
      "type": "text",
      "meta": {},
      "value": "Eindhoven",
      "timestamp": 1744879235088
    },
    "street": {
      "name": "street",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "postalCode": {
      "name": "postalCode",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    },
    "model": {
      "name": "model",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744879257359
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878843595
    }
  }
},
{
  "id": "6lDPL8mEyissE1cLzxz5Zr",
  "version": 3,
  "createdOn": 1744878834634,
  "name": "Fontys TQ",
  "accessPublicRead": false,
  "parentId": "56SzD7ckLvgQe8WAXDe5uE",
  "realm": "master",
  "type": "BuildingAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE",
    "6lDPL8mEyissE1cLzxz5Zr"
  ],
  "attributes": {
    "area": {
      "name": "area",
      "type": "positiveInteger",
      "meta": {
        "ruleState": true
      },
      "value": 10,
      "timestamp": 1744879341122
    },
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "city": {
      "name": "city",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "street": {
      "name": "street",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "postalCode": {
      "name": "postalCode",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878834623
    }
  }
},
{
  "id": "56SzD7ckLvgQe8WAXDe5uE",
  "version": 2,
  "createdOn": 1744878993725,
  "name": "Eindhoven",
  "accessPublicRead": false,
  "realm": "master",
  "type": "CityAsset",
  "path": [
    "56SzD7ckLvgQe8WAXDe5uE"
  ],
  "attributes": {
    "country": {
      "name": "country",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    },
    "notes": {
      "name": "notes",
      "type": "text",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    },
    "total_area": {
      "name": "total_area",
      "type": "integer",
      "meta": {
        "ruleState": true
      },
      "value": 30,
      "timestamp": 1744879415190
    },
    "location": {
      "name": "location",
      "type": "GEO_JSONPoint",
      "meta": {},
      "value": null,
      "timestamp": 1744878993716
    }
  }
}]
    """)
import os

import aiohttp
from tartiflette import TartifletteError

API_BASE_URL = "https://api.trello.com/1/"
TRELLO_API_KEY = os.environ["TRELLO_API_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]


class WebserviceError(TartifletteError):
    def __init__(self, message, status, extensions) -> None:
        super().__init__(
            message="%s [%s]: %s" % (API_BASE_URL, status, message),
            extensions=extensions,
        )


async def send_request(endpoint, payload):
    try:
        # aiohttp likes only string & int, transform any bool to JSON compatible string
        for k, v in list(payload.items()):
            if isinstance(v, bool):
                payload[k] = str(v).lower()
            if v is None:
                payload[k] = ""
        payload["key"] = TRELLO_API_KEY
        payload["token"] = TRELLO_TOKEN

        url = API_BASE_URL + endpoint
        extensions = {"endpoint": endpoint, "url": url}
        print("request:", url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as r:
                status = r.status
                if status != 200:
                    raise WebserviceError(
                        "http error (%s)" % await r.text(), status, {}
                    )
                try:
                    json_body = await r.json(content_type=None)
                except Exception:
                    extensions["text"] = await r.text()
                    raise WebserviceError("ws error", status, extensions)
                # print("JSON response:", json_body)
                return json_body
    except WebserviceError as e:
        return e
    except Exception:
        raise

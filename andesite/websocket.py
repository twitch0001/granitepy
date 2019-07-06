import json
import logging

import websockets
from discord.ext import commands

from . import events

log = logging.getLogger(__name__)


class WebSocket:
    def __init__(
        self, bot: commands.Bot, host: str, port: int, password: str, node
    ):
        self.bot = bot
        self.host = host
        self.port = port
        self.password = password
        self.user_id = bot.user.id
        self._connection_id = None

        self.metadata = None

        self._ws = None
        self._task = None
        self._closed = False

        self.headers = {
            "Authorization": password,
            "Andesite-Resume-Id": self._connection_id,
            "User-Id": self.user_id
        }

        self._node = node

    @property
    def is_connected(self):
        return self._ws is not None and self._ws.open

    async def _connect(self):
        await self.bot.wait_until_ready()

        uri = f"ws://{self.host}:{self.port}/websocket"

        try:
            self._ws = await websockets.connect(uri=uri, extra_headers=self.headers)
        except Exception as er:
            return log.warning(er)

        if not self._task:
            self._task = self.bot.loop.create_task(self._listen())

        self._closed = False

        log.debug(f"WEBSOCKET | Connection established to {uri}")

    async def _listen(self):
        while True:
            try:
                data = await self._ws.recv()
            except websockets.ConnectionClosed as e:
                if e.code == 4001:
                    log.warning("WEBSOCKET | Incorrect authentication")
                    break

                elif e.code == 4002:
                    log.warning(
                        f"WEBSOCKET | Closed with code 4002, attempting reconnect"
                    )
                    await self._connect()
                    break

                else:
                    log.warning(f"WEBSOCKET | Closed with code {e.code}")
                    break

            if data:
                data = json.loads(data)

                op = data.get("op", None)
                if op == "connection-id":
                    self._connection_id = data.get("id")
                    log.debug(
                        f"WEBSOCKET | Received connection-id of {self._connection_id}"
                    )

                elif op == "metadata":
                    self.metadata = data["data"]
                    log.debug("WEBSOCKET | Received metadata payload.")

                elif op == "player-update":
                    try:
                        await self._node.players[int(data["guildId"])].update_state(
                            data
                        )
                    except Exception as er:
                        log.warning(f"WEBSOCKET | Error in player-state data {data}")

                elif op == "event":
                    await self._event_dispatcher(data)

                else:
                    log.debug(f"WEBSOCKET | Unknown OP {op} returned {data}")

    async def _event_dispatcher(self, data):
        player = self._node.players[
            int(data["guildId"])
        ]  # getting the player that all events use, apart from websocket close.

        event = getattr(events, data["type"], None)

        if event is None:
            log.debug("WEBSOCKET | Unknown event %s, discarding", data["type"])
            return
        
        log.debug("WEBSOCKET | Dispatching event %s for guildId %s", data['type'], data['guildId'])

        await self._node._client.dispatch(event(player, data))

    async def _send(self, **data):
        if self.is_connected:
            log.debug(f"WEBSOCKET | Sending payload {data}")
            await self._ws.send(json.dumps(data))

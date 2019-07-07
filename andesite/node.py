import logging

import aiohttp
from discord.ext import commands

from .objects import Playlist, Track
from .websocket import WebSocket

log = logging.getLogger(__name__)


class Node:
    def __init__(
            self,
            host: str,
            port: int,
            user_id: int,
            *,
            client,
            rest_uri: str,
            password,
            identifier,
            shard_id=None
    ):
        self.rest_uri = rest_uri
        self.host = host
        self.port = port
        self.user_id = user_id
        self.identifier = identifier
        self.password = password
        self.shard_id = shard_id

        self._client = client
        self.session = None

        self.players = {}

        self._websocket = None

        self.available = True

    def __repr__(self):
        p_count = len(self.players.keys())
        return f"<GraniteNode player_count={p_count} available={self.available} shard_id={self.shard_id}>"

    def __str__(self):
        return self.identifier

    async def connect(self, bot: commands.Bot):
        self._websocket = WebSocket(
            bot, self.host, self.port, self.password, self
        )

        self.session = aiohttp.ClientSession(loop=self.loop)
        await self._websocket._connect()
        log.debug(f"NODE | Connected {self.__repr__()}")

    async def get_tracks(self, query: str):
        password = "null" if not self.password else self.password

        async with self.session.get(f"{self.rest_uri}/loadtracks", params=dict(identifier=query),
                                    headers={"Authorization": password}) as response:
            data = await response.json()

        if data.get('tracks', None) is None:
            log.info(f"REST | No results found for <{query}>")
            return None

        if data['loadType'] == 'PLAYLIST_LOADED':
            return Playlist(data=data)

        tracks = []
        for track in data["tracks"]:
            tracks.append(Track(_id=track["track"], data=track["info"]))

        log.debug(f"REST | Found <{len(tracks)}> results for query: <{query}>")

        return tracks

import json
import logging
import time

from discord.ext import commands

from .filters import Filter

logger = logging.getLogger(__name__)


class Player:
    """Handles every single connection, websocket, node and so on.

    Parameters
    ----------
    bot: :class:`commands.Bot`
    guild_id: :class:`int`
    node: :class:`.Node`

    Attributes
    ----------
    bot: :class:`commands.Bot`
    guild_id: :class:`int`
    node: :class:`.Node`
    last_update: Optional[:class:`float`]
    last_position: Optional[:class:`int`]
    last_state: ?
    position_timestamp: Optional[:class:`int`]
    volume: :class:`int`
    paused: :class:`bool`
    current: Optional[:class:`.Track`]
    channel_id: Optional[:class:`int`]"""
    def __init__(self, bot: commands.bot, guild_id: int, node):
        self.bot = bot
        self.guild_id = guild_id
        self.node = node

        self.last_update = None
        self.last_position = None
        self.last_state = None
        self.position_timestamp = None

        self._voice_state = {}

        self.volume = 100
        self.paused = False
        self.current = None
        self.channel_id = None

    @property
    def is_connected(self):
        """Determines if the player is currently connected to a channel.

        Returns
        -------
        :class:`bool`"""
        return self.channel_id is not None

    async def update_state(self, state: dict):
        state = state["state"]

        self.last_state = state
        self.last_update = time.time() * 1000
        self.last_position = state.get("position", 0)
        self.position_timestamp = state.get("time", 0)

    async def _voice_server_update(self, data):
        self._voice_state.update({"event": data})
        await self._dispatch_voice_update()

    async def _voice_state_update(self, data):
        self._voice_state.update({"sessionId": data["session_id"]})


        if data['channel_id'] is None:
            self.channel_id = None
        else:
            self.channel_id = int(data["channel_id"])

        if not self.channel_id:
            self._voice_state.clear()
            return logger.debug("PLAYER | Player-update with no channel_id, Clearing state")

        await self._dispatch_voice_update()

    async def _dispatch_voice_update(self):
        if {"sessionId", "event"} == self._voice_state.keys():
            logger.debug(f"PLAYER | Updating voice-state")
            await self.node._websocket._send(
                op="voice-server-update",
                guildId=str(self.guild_id),
                **self._voice_state,
            )

    async def connect(self, channel_id: int):
        """Connects to a Discord Voice Channel.

        Parameters
        ----------
        channel_id: :class:`int`
            The channel to connect to.

        Raises
        ------
        ValueError
            This player's guild id was invalidated.
        """
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            raise ValueError(f"Invalid guild id {self.guild_id}")

        self.channel_id = channel_id

        ws = self.bot._connection._get_websocket(guild.id)
        await ws.voice_state(self.guild_id, str(channel_id))

        logger.info(f"PLAYER | Connected to voice channel:  {channel_id}")

    async def disconnect(self):
        """Disconnects the player from the Voice Channel."""
        ws = self.bot._connection._get_websocket(self.guild_id)
        await ws.voice_state(self.guild_id, None)

    async def set_filters(self, filter_type):
        """.. note:: twitch wtf is a filter

        Raises
        ------
        TypeError
            The filter type was not a subclass of :class:`.Filter`"""
        if not issubclass(filter_type.__class__, Filter):
            raise TypeError("All filters must derive from `Filter`")

        await self.node._websocket._ws.send(json.dumps({'op': 'filters', **filter_type._payload, 'guildId': str(self.guild_id)}))
        logger.debug(f"PLAYER | Setting filter to <{filter_type}> for player <{self.guild_id}>")

    async def play(self, track):
        """Begin playing a track.

        Parameters
        ----------
        track: :class:`.Track`
            The track to play."""
        self.last_update = 0
        self.last_position = 0
        self.position_timestamp = 0
        self.paused = False

        self.current = track

        await self.node._websocket._send(
            op="play", guildId=str(self.guild_id), track=track.id
        )
        logger.debug(f"PLAYER | Now playing {track.title} in {self.channel_id}")

    async def set_pause(self, pause):
        """Pauses the player.

        Parameters
        ----------
        pause: :class:`bool`
            True to pause the player, or False to un-pause."""
        if pause is self.paused:
            return

        self.paused = pause

        await self.node._websocket._send(
            op="pause", pause=pause, guildId=str(self.guild_id)
        )

    async def seek(self, position):
        """Seeks to a specific point in the playing track.

        Parameters
        ----------
        position: :class:`int`
            The position, in milliseconds, to seek to.

        Raises
        ------
        ValueError
            The specified position was in an invalid range."""
        if not 0 <= position <= self.current.length:
            raise ValueError(
                "Position cannot be smaller than 0 or larger than track's length"
            )

        await self.node._websocket._send(
            op="seek", position=position, guildId=str(self.guild_id)
        )

    async def set_volume(self, volume):
        """Changes the volume to your specified one.

        Parameters
        ----------
        volume: :class:`int`
            The volume to change to."""
        await self.node._websocket._send(
            op="volume", volume=volume, guildId=str(self.guild_id)
        )

    async def stop(self):
        """Stops the player and kills the song."""
        await self.node._websocket._send(op="stop", guildId=str(self.guild_id))

    async def get_tracks(self, query: str):
        """Search for all tracks in that query.

        Parameters
        ----------
        query: :class:`str`
            The query to search for

        Returns
        -------
        Union[:class:`.Playlist`, List[:class:`.Track`]]
            Either a Playlist containing tracks, or a list of tracks to play."""
        return await self.node.get_tracks(query)

    async def destroy(self):
        """Kills the player, disconnecting and stopping the active track."""
        await self.stop()
        await self.disconnect()
        await self.node._websocket._send(op="destroy", guildId=str(self.guild_id))
        del self.node.players[self.guild_id]

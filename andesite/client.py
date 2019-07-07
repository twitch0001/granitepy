import asyncio
import logging

from discord.ext import commands

from .events import Event
from .exceptions import NodesUnavailable
from .node import Node
from .player import Player

log = logging.getLogger(__name__)


class Client:
    _event_hooks = {}

    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.loop = bot.loop or asyncio.get_event_loop()

        self.nodes = {}

        bot.add_listener(self.update_handler, "on_socket_response")

    def __repr__(self):
        player_count = len(self.players.values())
        return f"<GraniteClient player_count={player_count}>"

    @property
    def players(self):
        return self._get_players()

    def _get_players(self):
        players = []

        for node in self.nodes.values():
            players.extend(node.players.values())

        return {player.guild_id: player for player in players}

    async def start_node(
        self, host: str, port: int, *, rest_uri: str, password: str, identifier
    ):
        await self.bot.wait_until_ready()

        node = Node(
            host,
            port,
            self.bot.user.id,
            client=self,
            rest_uri=rest_uri,
            password=password,
            identifier=identifier,
        )
        await node.connect(self.bot)

        node.available = True

        self.nodes[identifier] = node

        return node

    def get_player(self, guild_id: int, cls=None):
        try:
            player = self.players[guild_id]
        except KeyError:
            pass
        else:
            return player

        guild = self.bot.get_guild(guild_id)

        if not guild:
            raise ValueError("Invalid guild_id passed.")

        if not self.nodes:
            raise NodesUnavailable("No nodes avaiable.")

        nodes = list(self.nodes.values())
        if not cls:
            cls = Player

        player = cls(self.bot, guild_id, nodes[0])
        nodes[0].players[guild_id] = player

        return player

    async def update_handler(self, data):
        if not data:
            return

        if data["t"] == "VOICE_SERVER_UPDATE":
            guild_id = int(data["d"]["guild_id"])
            try:
                player = self.players[guild_id]
            except KeyError:
                pass
            else:
                await player._voice_server_update(data["d"])

        elif data["t"] == "VOICE_STATE_UPDATE":
            # logger.warning(data)
            if int(data["d"]["user_id"]) != self.bot.user.id:
                return

            guild_id = int(data["d"]["guild_id"])
            try:
                player = self.players[guild_id]
            except KeyError:
                pass

            else:
                await player._voice_state_update(data["d"])
        else:
            return

    async def dispatch(self, event: Event):
        """
        Dispatches events, WIP.
        """
        event_name = "andesite_" + event.name
        self.bot.dispatch(event_name, event)

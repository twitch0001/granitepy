class Event:
    """Base event class.
    This class itself is never dispatched, but its subclasses are."""
    name = "null_event"


class TrackStartEvent(Event):
    """Dispatched on the TrackStartEvent sent from andesite.

    Attributes
    ----------
    name: :class:`str`
        The name of this event.
    player: :class:`.Player`
        The player relevant to this event.
    track: :class:`.Track`
        The track that started playing.
    """

    def __init__(self, player, data):
        self.name = "track_start"
        self.player = player
        self.track = data["track"]


class TrackEndEvent(Event):
    """Dispatched when a track has finished playing.

    Attributes
    ----------
    name: :class:`str`
        The name of this event.
    player: :class:`.Player`
        The player relevant to this event.
    track: :class:`.Track`
        The track that has finished playing.
    reason: :class:`str`
        Why the track has stopped.
    may_start_next: :class:`bool`

    """

    def __init__(self, player, data):
        self.name = "track_end"
        self.player = player
        self.track = data["track"]
        self.reason = data["reason"]
        self.may_start_next = data["mayStartNext"]


class TrackStuckEvent(Event):
    """.. note:: figure out what this means

    Attributes
    ----------
    name: :class:`str`
        This event's name.
    player: :class:`.Player`
        This event's relevant player.
    track: :class:`.Track`
        This event's relevant track.
    threshold: :class:`int`
        Unsure as of right now.
    """
    def __init__(self, player, data):
        self.name = "track_stuck"
        self.player = player
        self.track = data["track"]
        self.threshold = data["thresholdMs"]


class TrackExceptionEvent(Event):
    """Dispatched when a playing track raises an exception.

    Attributes
    ----------
    name: :class:`str`
        This event's name.
    player: :class:`.Player`
        This event's relevant player.
    error: :class:`str`
        The error that was raised during playing.
    exception
        The exception.
    """
    def __init__(self, player, data):
        self.name = "track_exception"
        self.player = player
        self.error = data["error"]
        self.exception = data["exception"]


class WebSocketClosedEvent(Event):
    """Dispatched when the websocket has closed.

    Attributes
    ----------
    name: :class:`str`
        This event's name.
    player: :class:`.Player`
        This event's relevant player.
    reason: :class:`str`
        The reason the websocket was closed.
    code: :class:`int`
        The websocket close code.
    by_remote: :class:`bool`
        Whether the websocket was closed remotely.
    """
    def __init__(self, player, data):
        self.name = "websocket_closed"
        self.player = player
        self.reason = data["reason"]
        self.code = data["code"]
        self.by_remote = data["byRemote"]

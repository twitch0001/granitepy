class Event:
    """Base event class"""


class TrackStartEvent(Event):
    """Dispatched on the TrackStartEvent sent from andesite."""

    name = "track_start"

    def __init__(self, player, data):
        self.player = player
        self.track = data["track"]


class TrackEndEvent(Event):
    name = "track_end"

    def __init__(self, player, data):
        self.player = player
        self.track = data["track"]
        self.reason = data["reason"]
        self.may_start_next = data["mayStartNext"]


class TrackStuckEvent(Event):
    name = "track_stuck"

    def __init__(self, player, data):
        self.player = player
        self.track = data["track"]
        self.threshold = data["thresholdMs"]


class TrackExceptionEvent(Event):
    name = "track_exception"

    def __init__(self, player, data):
        self.player = player
        self.error = data["error"]
        self.exception = data["exception"]


class WebSocketClosedEvent(Event):
    name = "websocket_closed"

    def __init__(self, player, data):
        self.player = player
        self.reason = data["reason"]
        self.code = data["code"]
        self.by_remote = data["byRemote"]

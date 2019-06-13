class Event:
    """Base event class"""


class TrackStartEvent(Event):
    """Dispatched on the TrackStartEvent sent from andesite."""

    name = "track_start"

    def __init__(self, player, track):
        self.player = player
        self.track = track


class TrackEndEvent(Event):
    name = "track_end"

    def __init__(self, player, track, reason, may_start_next):
        self.player = player
        self.track = track
        self.reason = reason
        self.may_start_next = may_start_next


class TrackStuckEvent(Event):
    name = "track_stuck"

    def __init__(self, player, track, threshold):
        self.player = player
        self.track = track
        self.threshold = threshold


class TrackExceptionEvent(Event):
    name = "track_exception"

    def __init__(self, player, error, exception):
        self.player = player
        self.error = error
        self.exception = exception


class WebSocketClosedEvent(Event):
    name = "websocket_closed"

    def __init__(self, player, reason, code, by_remote):
        self.player = player
        self.reason = reason
        self.code = code
        self.by_remote = by_remote

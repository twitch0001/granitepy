class Event:
    """Base event class"""


class TrackStartEvent(Event):
    """Dispatched on the TrackStartEvent sent from andesite."""

    name = "track_start"

    def __init__(self, player, track):
        self.player = player
        self.track = track

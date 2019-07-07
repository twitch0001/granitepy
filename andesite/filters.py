class Filter:
    # TODO: Add comparisons
    pass


class Equalizer(Filter):
    def __init__(self, band, gain):
        pass


class Karaoke(Filter):
    def __init__(self, *, level, mono_level, filter_band, filter_width):
        self.level = level
        self.mono_level = mono_level
        self.filter_band = filter_band
        self.filter_width = filter_width

        self._payload = {"karaoke": {"level": self.level,
                                     "monoLevel": self.mono_level,
                                     "filterBand": self.filter_band,
                                     "filterWidth": self.filter_width}}


class Timescale(Filter):
    def __init__(self, *, speed, pitch, rate):
        if not speed > 0:
            pass

        if not pitch > 0:
            pass

        if not rate > 0:
            pass

        self.speed = speed
        self.pitch = pitch
        self.rate = rate

        self._payload = {"timescale": {"speed": self.speed,
                                       "pitch": self.pitch,
                                       "rate": self.rate}}


class Tremolo(Filter):
    def __init__(self, *, frequency, depth):
        if not frequency > 0:
            pass

        if not 0 < depth <= 1:
            pass

        self.frequency = frequency
        self.depth = depth

        self._payload = {"tremolo": {"frequency": self.frequency,
                                     "depth": self.depth}}


class Vibrato(Filter):
    def __init__(self, *, frequency, depth):
        if not 0 < frequency <= 14:
            pass

        if not 0 < depth <= 1:
            pass

        self.frequency = frequency
        self.depth = depth

        self._payload = {"vibrato": {"frequency": self.frequency,
                                     "depth": self.depth}}

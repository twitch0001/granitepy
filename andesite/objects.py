class Track:
    def __init__(self, _id, data: dict):
        self.id = _id
        self.data = data

        self.title = data.get("title")
        self.author = data.get("author")
        self.length = data.get("length")
        self.yt_id = data.get("identifier")
        self.uri = data.get("uri")
        self.is_stream = data.get("isStream")
        self.is_seekable = data.get("isSeekable")
        self.position = data.get("position")

    def __str__(self):
        return self.title


    def __repr__(self):
        return "<Track length={0.length} is_stream={0.is_stream}>".format(self)


class Playlist:
    """Playlist Object.

    data - A dict returned from andesite
    tracks - list of andesite.Track
    """
    def __init__(self, data: dict):
        self.data = data

        self.name = data['playlistInfo']['name']

        self.tracks = [Track(_id = track['track'], data = track['info']) for track in data['tracks']]


    def __str__(self):
        return self.name


    def __repr__(self):
        return "<Playlist name={0.name}>".format(self)

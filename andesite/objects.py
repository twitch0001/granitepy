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

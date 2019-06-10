class Track:
    def __init__(self, _id, data: dict):
        self.id = _id
        self.data = data

        self.title = data.get("title")
        self.uri = data.get("uri")
        self.yt_id = data.get("identifier")

    def __str__(self):
        return self.title

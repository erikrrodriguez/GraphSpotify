from track import Track

class Album:
    def __init__(self, artist_query=None, album_query=None):
        self.artist_query = artist_query
        self.album_query = album_query

        #self.artist = Artist()
        self.tracks = []

    # These methods should check to make sure the result
    # has the attribute before loading that data...

    def load_spotify(self, result):
        self.title = result["name"]

        self.spotify = {}
        self.spotify["id"] = result["id"]
        self.spotify["url"] = result["external_urls"]["spotify"]

        self.artist = result["artists"][0]["name"]
        #self.artist.load_spotify(result["artists"][0])

        if "tracks" in result:
            for track in result["tracks"]:
                track = Track().load_spotify(track)
                self.tracks.append(track)

        return self

    def load_lastfm(self, result):
        self.listeners = result.get_listener_count()
        self.plays = result.get_playcount()

        return self

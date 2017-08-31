from album import Album
import sys

class Artist:
    def __init__(self):
        self.albums = []

    # TODO: these methods should check to make sure the result
    # has the attribute before loading that data...
    def load_spotify(self, result):
        self.title = result["name"]

        self.spotify = {}
        self.spotify["id"] = result["id"]
        self.spotify["url"] = result["external_urls"]["spotify"]

        if "popularity" in result:
            self.popularity = result["popularity"]

        # TODO: handle duplicate albums
        if "albums" in result:
            for album in result["albums"]:
                album = Album().load_spotify(album)
                self.albums.append(album)

        return self


    def load_lastfm(self, result):
        self.listeners = result.get_listener_count()
        self.plays = result.get_playcount()

        return self

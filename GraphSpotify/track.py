class Track:
    def __init__(self):
        pass

    # TODO: these methods should check to make sure the result
    # has the attribute before loading that data...
    def load_spotify(self, result):
        self.title = result["name"]

        self.spotify = {}
        self.spotify["id"] = result["id"]
        self.spotify["url"] = result["external_urls"]["spotify"]

        # TODO: this includes extra data we don't want, should strip it so
        # we don't use unnecessary memory
        self.audio_features = result["audio_features"]

        return self

#    def load_lastfm(self, result):
#        self.listeners = result.get_listener_count()
#        self.plays = result.get_playcount()

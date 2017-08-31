import pylast

class LastFM:
    def __init__(self, logger, api_key, api_secret):
        self.logger = logger
        self.network = pylast.LastFMNetwork(api_key, api_secret)

    def get_album(self, artist, album):
        self.logger.debug("Searching LastFM for <%s> by <%s>..."
                          % (album, artist))
        album = self.network.get_album(artist, album)
# TODO: log if network.get_album returns 0
        return album


    def get_artist(self, artist):
        self.logger.debug("Searching LastFM for artist <%s>..." % artist)
        artist = self.network.get_artist(artist)
# TODO: log if network.get_artist returns 0
        return artist

    # Left for compatibility with main.py
    def get_track_listeners_plays(self, artist, track):
        track = self.network.get_track(artist, track)
        listeners = track.get_listener_count()
        plays = track.get_playcount()
        return listeners, plays

    # Left for compatibility with main.py
    def get_album_listeners_plays(self, artist, album):
        listeners = self.network.get_album(artist, album).get_listener_count()
        plays = self.network.get_album(artist, album).get_playcount()
        return listeners, plays

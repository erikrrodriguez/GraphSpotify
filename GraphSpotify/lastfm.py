import pylast

class LastFM:

    def __init__(self, logger, api_key, api_secret):
        self.logger = logger
        self.network = pylast.LastFMNetwork(api_key, api_secret)


    # TODO: get listeners & plays for each track on album
    def get_album(self, album):
        artist_query = album["artist_query"].replace("+", " ")
        album_query = album["album_query"].replace("+", " ")

        self.logger.debug("Searching LastFM for <%s> by <%s>..."
                          % (album_query, artist_query))
        # TODO: log error if network.get_album returns 0
        # pylast throws some exception like pylast.WSError: Album not found
        album = self.network.get_album(artist_query, album_query)
        return {
            "listeners" : album.get_listener_count(),
            "plays" : album.get_playcount()
        }


    def get_artist(self, artist):
        artist_query = artist["artist_query"].replace("+", " ")

        self.logger.debug("Searching LastFM for artist <%s>..."
                          % artist_query)
        artist = self.network.get_artist(artist_query)
        # TODO: log error if network.get_artist returns 0

        return {
            "listeners" : artist.get_listener_count(),
            "plays" : artist.get_playcount()
        }


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

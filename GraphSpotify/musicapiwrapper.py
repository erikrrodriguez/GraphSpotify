from lastfm import LastFM
from spotify import Spotify
from dev_settings import *

# Returns dictionaries from queries
# In theory, all dictionaries should be easily convertable to JSON
# Query examples:
#   { "artist" : "the+xx" }
#   { "artist" : "the+xx", "album" : "coexist" }

class MusicApiWrapper:

    def __init__(self, logger):
        self.logger = logger
        self.lastfm = LastFM(logger, LAST_FM_API_KEY, LAST_FM_SECRET)
        self.spotify = Spotify(logger, SPOTIFY_CLIENT_ID,
                               SPOTIFY_CLIENT_SECRET)


    def get(self, query):
        self.logger.debug("Getting query <%s>." % repr(query))
        query = self.plus_to_space(query)
        self.logger.debug("Processed to <%s>." % repr(query))

        if "artist" in query and "album" in query:
            return self.get_album(query["artist"], query["album"])

        elif "artist" in query:
            return self.get_artist(query["artist"])

        return False


    def get_album(self, artist_query, album_query):
        self.logger.debug("Getting album <%s> by <%s>..."
                          % (album_query, artist_query))

        album = {
            "type" : "album",
            "artist_query" : artist_query,
            "album_query" : album_query
            }

        # Check album exists and get Spotify data if it does
        result = self.spotify.get_album(artist_query, album_query)
        if not result:
            self.logger.debug("No album found, returning False.")
            return False
        album.update(result)

        album.update( self.lastfm.get_album(album) )

        return album


    def get_artist(self, artist_query):
        self.logger.debug("Getting artist <%s>..." % artist_query)

        artist = { "type" : "artist", "artist_query" : artist_query }

        # Check artist exists and get Spotify data if it does
        result = self.spotify.get_artist(artist_query)
        if not result:
            self.logger.debug("No artist found, returning False.")
            return False
        artist.update(result)

        artist.update( self.lastfm.get_artist(artist) )

        return artist

    # E.g., "The+xx" to "The xx"
    def plus_to_space(self, dictionary):
        # Probably a way to do this with list comprehensions, but I'm just not
        # there yet... :)
        for key in dictionary:
            dictionary[key] = dictionary[key].replace("+", " ")
        return dictionary

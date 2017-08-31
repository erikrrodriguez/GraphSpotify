from lastfm import LastFM
from spotify import Spotify
from dev_settings import *
from album import Album
from artist import Artist
from track import Track

# Returns objects from queries
# It pulls from APIs to build rich Artist(), Album(), and Track() objects
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

        # Request for album?
        if "artist" in query and "album" in query:
            return self.get_album(query["artist"], query["album"])
        elif "artist" in query:
            return self.get_artist(query["artist"])

        return False


    def get_album(self, artist_query, album_query):
        self.logger.debug("Getting album <%s> by <%s>..."
                          % (album_query, artist_query))

        result = {"artist_query" : artist_query, "album_query" : album_query}
        album = Album(result)

        # Check album exists and get Spotify data if it does
        result = self.spotify.get_album(artist_query, album_query)
        if not result:
            self.logger.debug("No album found, returning False.")
            return False
        album.load(result)

        album.load( self.lastfm.get_album(album) )

        return album


    # TODO:
    def get_artist(self, artist_query):
        self.logger.debug("Getting artist <%s>..." % artist_query)

        artist = Artist({ "artist_query" : artist_query })

        # Check artist exists and get Spotify data if it does
        result = self.spotify.get_artist(artist_query)
        if not result:
            self.logger.debug("No artist found, returning False.")
            return False
        artist.load(result)

        artist.load( self.lastfm.get_artist(artist) )

        return artist

    # E.g., "The+xx" to "The xx"
    def plus_to_space(self, dictionary):
        # Probably a way to do this with list comprehensions, but I'm just not
        # there yet... :)
        for key in dictionary:
            dictionary[key] = dictionary[key].replace("+", " ")
        return dictionary

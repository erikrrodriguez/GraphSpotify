import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from artist import Artist
from track import Track

class Spotify:

    def __init__(self, logger, client_id, client_secret):
        self.logger = logger
        credentials = SpotifyClientCredentials(client_id, client_secret)
        self.network = spotipy.Spotify(client_credentials_manager=credentials)
        self.network.trace = False # what does this code do...?


    def get_album(self, artist_query, album_query):
        self.logger.debug("Searching Spotify for <%s> by <%s>..."
                          % (album_query, artist_query))

        query = "album:" + album_query + " artist:" + artist_query
        result = self.network.search(q=query, type="album", limit=1)
        albums = result["albums"]["items"]
        count = len(albums)
        self.logger.debug("Found %s albums." % count)
        if count == 0:
            return False

        return self.build_album_from(albums[0])


    def get_artist(self, artist):
        self.logger.debug("Searching Spotify for artist <%s>..." % artist)

        query = "artist:" + artist
        result = self.network.search(q=query, type="artist", limit=1)
        artists = result["artists"]["items"]
        count = len(artists)
        self.logger.debug("Found %s artists." % count)
        if count == 0:
            return False

        artist = artists[0]

        return { # TODO: include other information
            "name" : artist["name"],
            "albums" : self.get_artist_albums(artist["id"])
        }


    def get_artist_albums(self, artist_id):
        self.logger.debug("Searching for artist <%s>'s albums." % artist_id)

        result = self.network.artist_albums(artist_id=artist_id,
                                             album_type="album", limit=50)
        albums = result["items"]
        count = len(albums)
        self.logger.debug("Found %s albums." % count)
        if count == 0:
            return False

        # Have to do some extra processing here because Spotify sometimes
        # returns multiple versions of the same album...
        albums = self.filter_unique_albums(albums)

        albums = [self.build_album_from(album) for album in albums]

        return albums


    def get_tracks(self, id):
        self.logger.debug("Getting Spotify tracks for <%s>..." % id)
        result = self.network.album_tracks(id)
        count = result["total"]
        self.logger.debug("Found %s tracks." % count)
        if count == 0:
            self.logger.warn("Found no tracks for <%s>." % id)
            return False

        tracks = result["items"]
        tracks = self.get_audio_features(tracks)

        # TODO: limit to just information we want
        tracks = [Track(self.build_track_from(x)) for x in tracks]

        return tracks


    def get_audio_features(self, tracks):
        self.logger.debug("Getting audio features...")

        ids = [track["id"] for track in tracks]

        audio_features = self.network.audio_features(ids)

        for index, audio_feature in enumerate(audio_features):
            # Check IDs match, just to be sure
            if not audio_feature["id"] == tracks[index]["id"]:
                self.logger.error("Audio feature <%s> does not match "
                                  "track <%s>" % (tracks[index]["id"],
                                  audio_feature["id"]))
            tracks[index]["audio_features"] = audio_feature
        return tracks


    def build_album_from(self, result):
        artist = result["artists"][0]
        artist = { # TODO: include other information
            "name" : artist["name"]
        }

        album_query = result["name"].lower()
        album_query = urllib.parse.quote(album_query)
        album_query = album_query.replace("%20", "+")

        return { # TODO: include other information
            "name" : result["name"],
            "album_query" : album_query,
            "artist" : Artist(artist),
            "tracks" : self.get_tracks(result["id"]),
            "spotify" : {
                "id" : result["id"],
                "url" : result["external_urls"]["spotify"],
            }
        }


    def build_track_from(self, result):
        return {
            "name" : result["name"],
            "track_number" : result["track_number"],
            "audio_features" : result["audio_features"],
            "spotify" : {
                "id" : result["id"],
                "url" : result["external_urls"]["spotify"],
            }
        }


    def filter_unique_albums(self, albums):
        unique_albums = []
        unique_album_names = []

        for key, album in enumerate(albums):
            if not album["name"] in unique_album_names:
                unique_albums.append(album)
                unique_album_names.append(album["name"])

        return unique_albums

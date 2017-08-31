import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
    def __init__(self, logger, client_id, client_secret):
        self.logger = logger
        credentials = SpotifyClientCredentials(client_id, client_secret)
        self.network = spotipy.Spotify(client_credentials_manager=credentials)
        self.network.trace = False # what does this code do...?

    def get_album(self, artist, album):
        self.logger.debug("Searching Spotify for <%s> by <%s>..."
                          % (album, artist))

        query = "album:" + album + " artist:" + artist
        results = self.network.search(q=query, type="album", limit=1)
        results = results["albums"]["items"]
        count = len(results)
        self.logger.debug("Found %s results." % count)

        return False if count == 0 else results[0]

    def get_artist(self, artist):
        self.logger.debug("Searching Spotify for artist <%s>..." % artist)

        query = "artist:" + artist
        results = self.network.search(q=query, type="artist", limit=1)
        results = results["artists"]["items"]
        count = len(results)
        self.logger.debug("Found %s results." % count)

        return False if count == 0 else results[0]

    def get_artist_albums(self, artist):
        self.logger.debug("Searching for artist <%s>'s albums." % artist)

        results = self.network.artist_albums(artist_id=artist,
                                             album_type="album", limit=50)
        results = results["items"]
        count = len(results)
        self.logger.debug("Found %s results." % count)
        
        return False if count == 0 else results

    def get_tracks(self, id):
        self.logger.debug("Getting Spotify tracks for <%s>..." %id)
        results = self.network.album_tracks(id)
        self.logger.debug("Found %s results." % results["total"])
        tracks = results["items"]

        self.logger.debug("Getting audio features...")
        ids = self.get_ids(tracks)
        audio_features = self.network.audio_features(ids)
        tracks = self.append_audio_features(tracks, audio_features)

        return tracks

    def get_ids(self, tracks):
        ids = []
        for track in tracks:
            ids.append(track["id"])
        return ids

    def append_audio_features(self, tracks, audio_features):
        for index, audio_feature in enumerate(audio_features):
            # Check IDs match, just to be sure
            if not audio_feature["id"] == tracks[index]["id"]:
                self.logger.error("Audio feature <%s> does not match "
                                  "track <%s>" % (tracks[index]["id"],
                                  audio_feature["id"]))
            tracks[index]["audio_features"] = audio_feature
        return tracks

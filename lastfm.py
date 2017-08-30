from dev_settings import LAST_FM_API_KEY, LAST_FM_SECRET
import pylast
#
class LastFM:
    def __init__(self):
        self.network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_SECRET)

    def get_album_listeners_plays(self, artist, album):
        listeners = self.network.get_album(artist, album).get_listener_count()
        plays = self.network.get_album(artist, album).get_playcount()
        return listeners, plays

    def get_track_listeners_plays(self, artist, track):
        listeners = self.network.get_track(artist, track).get_listener_count()
        plays = self.network.get_track(artist, track).get_playcount()
        return listeners, plays

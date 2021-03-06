import spotipy
import string
import dev_settings
from lastfm import LastFM
from bokeh.plotting import * #Target Bokeh 0.12.5
from bokeh.models import *
from bokeh.layouts import *
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from math import pi

class Artist:
    def __init__(self, artist, search_type='artist'):
        self.type = 'artist'
        self.artist = artist
        self.name = self.artist['name']
        self.popularity = self.artist['popularity']
        self.genres = ','.join(self.artist['genres']) if len(self.artist['genres']) > 0 else ''
        self.albums = OrderedDict()
        self.search_albums()

    def search_albums(self):
        album_search = []
        print('searching artist albums...')
        results = sp.artist_albums(self.artist['id'], album_type='album')
        album_search.extend(results['items'])
        while results['next']: #if multiple spotify pages
            results = sp.next(results)
            album_search.extend(results['items'])
        print('searching album release dates...')
        for album in album_search: #get release date then sort
            result = sp.album(album['id'])
            album['release_date'] = result['release_date'][:4]
        album_search.sort(key=lambda album:int(album['release_date']))
        print('creating album classes...')
        for album in album_search: #make each album into class
            name = album['name'].replace(':','')
            self.albums[name] = Album(self.artist['name'], album, 'artist')
        print('calculating album plays...')
        max_plays = max([album.plays for album in self.albums.values()])
        for album in self.albums.values():
            album.scaled_plays = album.plays / max_plays
            album.features['plays'] = album.scaled_plays

    def print_all(self):
        print('====', self.name, '====')
        print('Popularity: ', self.popularity)
        print('Followers: ', self.artist['followers']['total'])
        print('Genres: ', self.genres)
        print('=====' + '='*len(self.name) + '=====')
        for album in self.albums.values():
            album.print_all()
            print()

class Album:
    def __init__(self, artist, album, search_type):
        self.type = 'album'
        self.search_type = search_type
        self.artist = artist
        self.album = album
        self.name = album['name'].translate(str.maketrans("", "", string.punctuation)) #bokeh labels can't handle certian chars
        if 'release_date' in self.album.keys():
            self.release_date = album['release_date']
            self.axis_label = self.name + ' (' + self.release_date + ')'
        self.features = {}
        self.tracks = OrderedDict()
        self.duration_ms = 0
        print('getting lastfm album data...')
        self.listeners, self.plays = lastfm.get_album_listeners_plays(artist, album['name'])
        # print('{}: listeners: {}, plays:{}.'.format(self.name, self.listeners, self.plays))
        self.scaled_plays = 0
        self.search_tracks()

    def search_tracks(self):
        print('searching tracks...')
        results = sp.album_tracks(self.album['id'])
        print('creating track classes...')
        for track in results['items']:
            self.tracks[track['name']] = Track(self.artist, track, self.search_type)
            self.duration_ms += track['duration_ms']
        if self.search_type is 'album': #only calc track plays if searching by album
            print('calculating track plays...')
            max_plays = max([track.plays for track in self.tracks.values()])
            for track in self.tracks.values():
                track.scaled_plays = track.plays / max_plays
                track.features['plays'] = track.scaled_plays
        self.calc_features()

    def calc_features(self):
        print('calculating weighted album features...')
        self.features = {'danceability':0, 'energy':0, 'loudness':0, 'mode':0, 'speechiness':0, 'acousticness':0, 'instrumentalness':0,
                               'liveness':0, 'valence':0, 'tempo':0, 'duration_ms':0, 'time_signature':0}
        for key in self.features: #average tracks
            for track in self.tracks:
                self.features[key] = self.features[key] + (self.tracks[track].features[key] 
                                                        * (self.tracks[track].duration_ms / self.duration_ms)) #weighted avg by duration

    def print_all(self):
        print((self.name + ' (' + self.release_date + ')'))
        for track in self.tracks.values():
            track.print_all()
        for key, value in self.features.items():
            print(key, " : ", round(value,2))

class Track:
    def __init__(self, artist, track, search_type):
        self.track = track
        self.artist = artist
        self.name = track['name']
        self.axis_label = track['name']
        self.duration_ms = track['duration_ms']
        if search_type is 'album':
            print('getting lastfm track data...')
            self.listeners, self.plays = lastfm.get_track_listeners_plays(artist, track['name'])
            self.scaled_plays = 0
        else:
            self.listeners = 0
            self.plays = 0
            self.scaled_plays = 0
        print('searching track features...')
        self.features = sp.audio_features(track['id'])[0]

    def print_all(self):
        print('    ' + self.name)

class Graph:
    def __init__(self):
        self.colors = ['red', 'yellow', 'blue', 'green', 'orange', 'brown', 'purple', 'black', 'white']
        self.selected_colors = ['red', 'yellow', 'blue', 'green', 'orange', 'brown', 'purple', 'black', 'white']
        self.graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence', 'Plays']
        self.selected_graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence', 'Plays']
        self.feat_color_dict = dict(zip(self.graph_features, self.colors))

        self.search_select = RadioButtonGroup(labels=["Artist", "Album"], active=0, width=200)
        self.text_input = TextInput(value="", title="", width=200)
        self.search_button = Button(label="Search",button_type="success", width=200)
        self.feature_choices = CheckboxButtonGroup(labels=self.graph_features, active=[0,1,2,3,4,5,6,7,8], width=50)
        self.controls = widgetbox(self.search_select, self.text_input, self.search_button, self.feature_choices)

        self.search_button.on_click(self.search_spotify)
        self.feature_choices.on_change('active', self.update_features)

        self.ds = []
        self.legend = []

        self.p = figure(title='Artist / Album',
                       x_range=[''], y_range=(0.0,1.03),
                       toolbar_location=None,
                       width=1000, height=1000,
                       responsive=True
                       )
        self.p.title.align = "center"
        self.p.background_fill_color = "gray"
        self.p.background_fill_alpha = 0.3
        self.p.yaxis.major_tick_line_color = None
        self.p.yaxis.minor_tick_line_color = None
        self.p.xaxis.major_tick_line_color = None
        self.p.xaxis.minor_tick_line_color = None
        self.p.xgrid.grid_line_color = None
        self.p.xaxis.axis_line_color = None
        self.p.yaxis.axis_line_color = None
        self.p.min_border_bottom = 100

        self.ml = self.p.multi_line(xs=[], ys=[], line_color=[])
        self.mlds = self.ml.data_source
        self.c = self.p.circle(x=[], y=[], size=15, fill_color=[])
        self.cds = self.c.data_source

        self.hover = HoverTool(tooltips=[('Val:', '@y')],
                                renderers=[self.c])

        self.p.tools.append(self.hover)

        self.layout = row(self.controls, self.p)

        curdoc().add_root(self.layout)
        curdoc().title = "Spotify Graph"


    def search_spotify(self):
        print('searching artist/album')
        self.ds = []
        if self.search_select.active == 0:
            results = sp.search(q='artist:' + self.text_input.value, type='artist', limit=1)
            items = results['artists']['items']
            print("searched artist")
            if len(items) > 0:
                self.ds = Artist(items[0], 'artist')
        else:
            results = sp.search(q='album:' + self.text_input.value, type='album', limit=1)
            print("searched album")
            items = results['albums']['items']
            if len(items) > 0:
                self.ds = Album(items[0]['artists'][0]['name'], items[0], 'album')
        if self.ds:
            self.update_data()

    def search_spotify2(self, name, type):
        if type is 'artist':
            results = sp.search(q='artist:' + name, type='artist', limit=1)
            items = results['artists']['items']
            print("searched artist")
            if len(items) > 0:
                self.ds = Artist(items[0])
        else:
            results = sp.search(q='album:' + name, type='album', limit=1)
            items = results['albums']['items']
            print("searched album")
            if len(items) > 0:
                self.ds = Album(items[0]['artists'][0]['name'],items[0])
        self.update_data()

    def update_features(self, attr, old, new):
        self.selected_graph_features = []
        self.selected_colors = []
        for num in self.feature_choices.active:
            self.selected_graph_features.append(self.graph_features[num])
        self.selected_colors = [self.feat_color_dict[key] for key in self.selected_graph_features]
        print('features updated')
        if self.ds:
            self.update_data()

    def update_data(self):
        print('graphing...')
        data = self.ds.albums if self.ds.type is 'artist' else self.ds.tracks
        x = []
        y = []
        lx = []
        ly = []
        for key, val in data.items():
            x.extend([val.axis_label]*len(self.selected_graph_features))
            y.extend([val.features[key] for key in val.features.keys() if key.capitalize() in self.selected_graph_features])
            lx.append([val.axis_label]*len(self.selected_graph_features))
            ly.append([val.features[key] for key in val.features.keys() if key.capitalize() in self.selected_graph_features])

        lines_x = [[val.axis_label for val in data.values()]]*len(self.selected_graph_features)
        lines_y = list(map(list,zip(*ly)))

        # self.build_legend(lx, ly)
        # i = 0 #Build Legend
        # for (colr, _x, _y) in zip(self.selected_colors, lx[0], ly[0]):
        #     self.p.circle([_x], [_y], size=15, fill_color=colr, legend=self.selected_graph_features[i])
        #     i += 1

        self.p.title.text = self.ds.name if self.ds.type is 'artist' else '{} by {}'.format(self.ds.name, self.ds.artist)
        self.p.title.align = "center"
        self.p.x_range.factors = [val.axis_label for val in data.values()]
        self.p.xaxis.axis_label = "Albums" if self.ds.type is 'artist' else 'Tracks'
        self.p.yaxis.axis_label = "Scaled Features"
        self.p.xaxis.axis_label_standoff = 20
        self.p.yaxis.axis_label_standoff = 20
        self.p.xaxis.major_label_orientation = pi/4
        
        self.mlds.data = dict(xs=lines_x, ys=lines_y, line_color=self.selected_colors)
        self.cds.data = dict(x=x, y=y, fill_color=self.selected_colors*len(data.values()))

client_credentials_manager = SpotifyClientCredentials(dev_settings.SPOTIFY_CLIENT_ID, dev_settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

lastfm = LastFM()
graph = Graph()
# graph.search_spotify2('the earth is not a cold dead place', 'album')
# graph.search_spotify2('Erbear', 'artist')




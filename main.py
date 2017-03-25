import spotipy
import string
import dev_settings
from bokeh.plotting import *
from bokeh.models import *
from bokeh.layouts import *
from spotipy.oauth2 import SpotifyClientCredentials
from collections import OrderedDict
from math import pi

client_credentials_manager = SpotifyClientCredentials(dev_settings.SPOTIFY_CLIENT_ID, dev_settings.SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

class Artist:
    def __init__(self, search):
        self.type = 'artist'
        self.artist = search
        self.name = self.artist['name']
        self.popularity = self.artist['popularity']
        self.genres = ','.join(self.artist['genres']) if len(self.artist['genres']) > 0 else ''
        self.albums = OrderedDict()
        self.search_albums()

    def search_albums(self):
        album_search = []
        results = sp.artist_albums(self.artist['id'], album_type='album')
        album_search.extend(results['items'])
        while results['next']: #if multiple spotify pages
            results = sp.next(results)
            album_search.extend(results['items'])
        for album in album_search: #get release date then sort
            result = sp.album(album['id'])
            album['release_date'] = result['release_date'][:4]
        album_search.sort(key=lambda album:int(album['release_date']))
        for album in album_search:
            name = album['name'].replace(':','')
            self.albums[name] = Album(album)

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
    def __init__(self, album):
        self.type = 'album'
        self.album = album
        self.name = album['name'].translate(str.maketrans("", "", string.punctuation))
        self.release_date = album['release_date']
        self.axis_label = self.name + ' (' + self.release_date + ')'
        self.features = {}
        self.tracks = OrderedDict()
        self.num_tracks = 0
        self.search_tracks()

    def search_tracks(self):
        results = sp.album_tracks(self.album['id'])
        for track in results['items']:
            self.tracks[track['name']] = Track(track)
        self.num_tracks = len(self.tracks)
        self.calc_features()

    def calc_features(self):
        self.features = {'danceability':0, 'energy':0, 'loudness':0, 'mode':0, 'speechiness':0, 'acousticness':0, 'instrumentalness':0,
                               'liveness':0, 'valence':0, 'tempo':0, 'duration_ms':0, 'time_signature':0}
        for key in self.features: #average tracks
            for track in self.tracks:
                self.features[key] = self.features[key] + (self.tracks[track].features[key] / self.num_tracks)

    def print_all(self):
        print((self.name + ' (' + self.release_date + ') : ' + str(self.num_tracks) + ' tracks'))
        for track in self.tracks.values():
            track.print_all()
        for key, value in self.features.items():
            print(key, " : ", round(value,2))

class Track:
    def __init__(self, track):
        self.track = track
        self.name = track['name']
        self.axis_label = track['name']
        self.features = sp.audio_features(track['id'])[0]

    def print_all(self):
        print('    ' + self.name)

def search_spotify():
    global data_source
    if search_select.active == 0:
        results = sp.search(q='artist:' + text_input.value, type='artist', limit=1)
        items = results['artists']['items']
        if len(items) > 0:
            data_source = Artist(items[0])
    else:
        results = sp.search(q='album:' + text_input.value, type='album', limit=1)
        items = results['albums']['items']
        if len(items) > 0:
            data_source = Album(items[0])
    update_data()

def update_features(attr, old, new):
    global selected_graph_features
    selected_graph_features = []
    for i in feature_choices.active:
        selected_graph_features.extend(graph_features[i])
    update_data()

def update_data():
    global data, x, y, lines_x, lines_y
    data = data_source.albums if data_source.type is 'artist' else data_source.tracks
    x = []
    y = []
    for key, val in data.items():
        x.append([val.axis_label]*len(selected_graph_features))
        y.append([val.features[key] for key in val.features.keys() if key.capitalize() in graph_features])

    lines_x = [[val.axis_label for val in data.values()]]*len(graph_features)
    lines_y = list(map(list,zip(*y)))
    graph_data()

def graph_data():
    global p, legend_items, legend
    p.title = data_source.name
    # p.width = min(200*len(data.keys()),1500)
    # p.height=750
    p.x_range = [val.axis_label for val in data.values()]
    p.xaxis.axis_label = "Albums" if search_select.active == 0 else 'Tracks'
    p.yaxis.axis_label = "Scaled Features"
    p.multi_line(lines_x, lines_y, color=colors, line_width=2)
    for i in range(len(x)):
        if i == 0:
            count = 0
            for (colr, leg, _x, _y ) in zip(colors, graph_features, x[0], y[0]):
                legend_items[count] = p.circle([_x], [_y], size=15, fill_color=colr)
                count += 1
        else:
            p.circle(x[i], y[i], size=15, fill_color=colors)
    
    # legend = Legend(items=zip(graph_features, legend_items), location=(0, 0), orientation="vertical")
    legend = Legend(items=[
            (graph_features[0], [legend_items[0]]),
            (graph_features[1], [legend_items[1]]),
            (graph_features[2], [legend_items[2]]),
            (graph_features[3], [legend_items[3]]),
            (graph_features[4], [legend_items[4]]),
            (graph_features[5], [legend_items[5]]),
            (graph_features[6], [legend_items[6]]),
            (graph_features[7], [legend_items[7]]),
        ], location=(0, 0), orientation="vertical")
    p.add_layout(legend, 'right')


colors = ['red', 'yellow', 'blue', 'green', 'orange', 'brown', 'purple', 'black']
graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence']
selected_graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence']

data_source = []
data = []
x = []
y = []
lines_x = []
lines_y = []
legend_items = [0]*len(feature_choices.active)
legend = []

# p = figure(title=data_source.name, 
#            x_range=[val.axis_label for val in data.values()], y_range=(0.0,1.0),
#            tools='pan,wheel_zoom',toolbar_location="above", toolbar_sticky=False,
           # width=min(200*len(data.keys()),1500), height=750)
p = figure(title='', 
           x_range=(0.0,1.0), y_range=(0.0,1.0),
           tools='pan, wheel_zoom',toolbar_location="above", toolbar_sticky=False,
           width=750, height=750)
p.title.align = "center"
p.xaxis.axis_label_standoff = 20
p.yaxis.axis_label_standoff = 20
p.xaxis.major_label_orientation = pi/4
p.background_fill_color = "gray"
p.background_fill_alpha = 0.5

search_select = RadioButtonGroup(labels=["Artist", "Album"], active=0)
text_input = TextInput(value="", title="")
search_button = Button(label="Search",button_type="success")
feature_choices = CheckboxButtonGroup(labels=graph_features, active=[])
controls = widgetbox(search_select, text_input, search_button, feature_choices)

search_button.on_click(search_spotify)
feature_choices.on_change('active', update_features)

# bokeh.plotting.reset_output
output_file("lines.html")
layout = row(controls, p)
show(layout)



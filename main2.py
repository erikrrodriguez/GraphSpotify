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
    print('clicked')
    global ds
    ds = []
    if search_select.active == 0:
        results = sp.search(q='artist:' + text_input.value, type='artist', limit=1)
        items = results['artists']['items']
        if len(items) > 0:
            ds = Artist(items[0])
    else:
        results = sp.search(q='album:' + text_input.value, type='album', limit=1)
        items = results['albums']['items']
        if len(items) > 0:
            ds = Album(items[0])
    print("searched")
    update_data(ds)

def search_spotify2(name):
    global ds
    if search_select.active == 0:
        results = sp.search(q='artist:' + name, type='artist', limit=1)
        items = results['artists']['items']
        if len(items) > 0:
            ds = Artist(items[0])
    else:
        results = sp.search(q='album:' + name, type='album', limit=1)
        items = results['albums']['items']
        if len(items) > 0:
            ds = Album(items[0])
    update_data(ds)

def update_features(attr, old, new):
    global selected_graph_features
    selected_graph_features = []
    for i in feature_choices.active:
        selected_graph_features.extend(graph_features[i])
    print('features updated')
    update_data()

def update_data(ds):
    data = ds.albums if ds.type is 'artist' else ds.tracks
    x = []
    y = []
    for key, val in data.items():
        x.extend([val.axis_label]*len(selected_graph_features))
        y.extend([val.features[key] for key in val.features.keys() if key.capitalize() in selected_graph_features])

    lines_x = [[val.axis_label for val in data.values()]]*len(selected_graph_features)
    chunk_size = len(selected_graph_features) #number of albums or tracks
    chunks = [y[i:i+chunk_size] for i in range(0, len(y), chunk_size)] #split y into list of chunks
    lines_y = list(map(list,zip(*chunks)))

    # print(x)
    # print()
    # print(lines_x)
    # print()
    # print(y)
    # print()
    # print(chunks)
    # print()
    # print(lines_y)
    # print()
    # print(len(lines_x), len(lines_y),len(colors[:len(selected_graph_features)]*int(len(data.values())/2)))

    p.title.text = ds.name
    p.title.align = "center"
    p.x_range.factors = [val.axis_label for val in data.values()]
    # p.width = max(750, min(200*len(data.keys()),1300))
    p.xaxis.axis_label = "Albums" if search_select.active == 0 else 'Tracks'
    p.yaxis.axis_label = "Scaled Features"
    p.xaxis.axis_label_standoff = 20
    p.yaxis.axis_label_standoff = 20
    p.xaxis.major_label_orientation = pi/4

    mlds.data = dict(xs=lines_x, ys=lines_y, line_color=colors[:len(selected_graph_features)]*int(len(data.values())/2))
    cds.data = dict(x=x, y=y, fill_color=colors[:len(selected_graph_features)]*len(data.values()))
    print('updated')

# def chunks(l, n):
#     Yield successive n-sized chunks from l.
#     for i in range(0, len(l), n):
#         yield l[i:i + n]

colors = ['red', 'yellow', 'blue', 'green', 'orange', 'brown', 'purple', 'black']
graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence']
selected_graph_features = ['Danceability', 'Energy', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness','Liveness', 'Valence']

search_select = RadioButtonGroup(labels=["Artist", "Album"], active=0)
text_input = TextInput(value="", title="")
search_button = Button(label="Search",button_type="success")
feature_choices = CheckboxButtonGroup(labels=graph_features, active=[0,1,2,3,4,5,6,7])
controls = widgetbox(search_select, text_input, search_button, feature_choices)

search_button.on_click(search_spotify)
feature_choices.on_change('active', update_features)

ds = []

p = figure(title='', 
           x_range=[''], y_range=(0.0,1.0),
           tools='pan, wheel_zoom',toolbar_location="above", toolbar_sticky=False,
           width=750, height=750)
p.title.text = "Artist / Album"
p.title.align = "center"
p.background_fill_color = "gray"
p.background_fill_alpha = 0.5

ml = p.multi_line(xs=[], ys=[], line_color=[])
mlds = ml.data_source
c  = p.circle(x=[], y=[], size=15, fill_color=[])
cds = c.data_source

# legend_items = [0]*len(feature_choices.active)
# legend = []

# search_spotify2("Flying Lotus")
layout = row(controls, p)

# output_file("lines.html")
# show(layout)

curdoc().add_root(layout)
curdoc().title = "Spotify Graph"



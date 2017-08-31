import string
from album import Album
from artist import Artist

# Returns template data from an object (Album, Artist, etc...)

def get_visualization(object):
    if object.__class__ == Album:
        return get_visualization_album(object)
    if object.__class__ == Artist:
        return get_visualization_artist(object)

    return False

def get_visualization_album(object):
    data = {}

    data["template"] = "album.html"
    data["artist_title"] = parse_chars(object.artist)
    data["album_title"] = parse_chars(object.title)
    data["listeners"] = object.listeners
    data["plays"] = object.plays

    return data

def get_visualization_artist(object):
    data = {}

    data["template"] = "artist.html"
    data["artist_title"] = parse_chars(object.title)
    data["listeners"] = object.listeners
    data["plays"] = object.plays

    data["albums"] = []
    for album in object.albums:
        data["albums"].append({ "title" : album.title })

    return data

def parse_chars(name):
    return name.translate(str.maketrans("", "", string.punctuation))

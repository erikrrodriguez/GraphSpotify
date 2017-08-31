import string
from album import Album
from artist import Artist

# Returns template dictionary from an object (Album, Artist, etc...)

def get_visualization(object):
    if object.__class__ == Album:
        return get_visualization_album(object)
    if object.__class__ == Artist:
        return get_visualization_artist(object)

    return False


def get_visualization_album(album):
    data = album.__dict__
    data["name"] = parse_chars(data["name"])

    data["artist"] = album.artist.__dict__
    data["artist"]["name"] = parse_chars(data["artist"]["name"])

    for key, track in enumerate(album.tracks):
        track = track.__dict__
        track["name"] = parse_chars(track["name"])
        data["tracks"][key] = track

    data["template"] = "album.html"
    return data


def get_visualization_artist(artist):
    data = artist.__dict__
    data["name"] = parse_chars(data["name"])

#    for album in artist.albums:
#        data["albums"].ap

    data["template"] = "artist.html"
    return data


# TODO: handle unusual chars without erasing
def parse_chars(name):
    return name.translate(str.maketrans("", "", string.punctuation))

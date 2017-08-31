import urllib
import string

# Returns template dictionary from another dict

def get_visualization(dict):
    if dict["type"] == "album":
        return get_visualization_album(dict)
    if dict["type"] == "artist":
        return get_visualization_artist(dict)

    return False


def get_visualization_album(album):
    album["template"] = "album.html"

    album["url"] = to_url(album["name"])
    album["artist"]["url"] = to_url(album["artist"]["name"])

    return album


def get_visualization_artist(artist):
    artist["template"] = "artist.html"

    artist["url"] = to_url(artist["name"])

    # probably replacable with a list comprehension??
    for key, album in enumerate(artist["albums"]):
        album["url"] = to_url(album["name"])
        artist["albums"][key] = album

    return artist


def to_url(name):
    # TODO: move this out of here - it really belongs in Flask somewhere
    url = name.lower()
    # Seems like flask does this ??
    #url = urllib.parse.quote(url)
    url = url.replace(" ", "+")
    return url

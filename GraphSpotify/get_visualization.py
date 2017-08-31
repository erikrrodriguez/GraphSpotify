import json

# Returns template dictionary from data

def get_visualization(data):
    if data["type"] in ["album", "artist"]:
        data["template"] = data["type"] + ".html"
        data["url"] = to_url(data["name"])

        data.pop("album_query", None) # security measure, DO NOT REMOVE
        data.pop("artist_query", None) # security measure, DO NOT REMOVE
        # Uncomment below to make the JSON output human-readable
        #data["json"] = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        data["json"] = json.dumps(data, separators=(',', ':'))

        return globals()["get_visualization_" + data["type"]](data)

    return False


def get_visualization_album(album):

    album["artist"]["url"] = to_url(album["artist"]["name"])

    return album


def get_visualization_artist(artist):
    # probably replacable with a list comprehension??
    for key, album in enumerate(artist["albums"]):
        album["url"] = to_url(album["name"])
        artist["albums"][key] = album

    return artist


def to_url(name):
    # TODO: move this out of here - it really belongs in Flask somewhere
    url = name.lower()
    url = url.replace(" ", "+")
    return url

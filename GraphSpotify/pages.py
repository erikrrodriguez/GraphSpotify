from visualizer import visualize

# Returns template dictionary from data

def get_page_visualize(music_api, query):
    data = music_api.get(query)

    if data["type"] in ["album", "artist"]:
        data["url"] = to_url(data["name"])

        data.pop("album_query", None) # security measure, DO NOT REMOVE
        data.pop("artist_query", None) # security measure, DO NOT REMOVE

        data["visualizer_js"], data["visualizer_html"] = visualize(data)
        data = globals()["get_page_visualize_" + data["type"]](data)
        return data["type"] + ".html", data

    return False, False


def get_page_visualize_album(album):
    album["artist"]["url"] = to_url(album["artist"]["name"])

    return album


def get_page_visualize_artist(artist):
    # probably replacable with a list comprehension??
    for key, album in enumerate(artist["albums"]):
        album["url"] = to_url(album["name"])
        artist["albums"][key] = album

    return artist


def to_url(name):
    url = name.lower()
    url = url.replace(" ", "+")
    return url

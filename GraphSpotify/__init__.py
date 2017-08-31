#from .GraphSpotify import app


#unused code below
"""
        data["artist_title"] = album_data["artists"][0]["name"]
        data["album_title"] = album_data["name"]
        data["listeners"] = listeners
        data["plays"] = plays

import urllib.parse
def name_to_slug(name):
    name = name.lower()
    return urllib.parse.quote_plus(name)

def slug_to_name(slug):
    return urllib.parse.unquote_plus(name)

def enable_logging(log_file, log_level):
    # TODO: fix permissions on this file to be more restrictive
    file_handler = FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(Formatter(
        "%(asctime)s %(levelname)s: %(pathname)s:"
        "%(lineno)d %(module)s:%(funcName)s %(message)s"))
    app.logger.addHandler(file_handler)

# Set some app-wide variables here

# TODO: change logging levels based on debug status
#       and alter this code to appear after enable_logging is defined
# TODO: move to separate configuration file
LOG_FILE = "/var/www/apps/SpotifyGraph/logs/SpotifyGraph.log"

if not app.debug:
    enable_logging(LOG_FILE, logging.DEBUG)
"""

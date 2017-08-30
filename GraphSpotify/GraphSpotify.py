import logging
from logging import FileHandler
from logging import Formatter

# bokeh import here

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    app.logger.debug("Serving home page.")
    return render_template("home.html")

# TODO:
@app.route("/artist/<id>")
def artist(id):
    app.logger.debug("Serving artist %s." % id)
    return "Page for artist: %s" % id

# TODO:
@app.route("/album/<id>")
def album(id):
    app.logger.debug("Serving album %s." % id)
    return "Page for album: %s" % id

# TODO:
#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('404.html'), 404

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

# Cleaner whitespace in rendered HTML
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

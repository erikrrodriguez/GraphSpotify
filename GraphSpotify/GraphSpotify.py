from musicapiwrapper import MusicApiWrapper
from get_visualization import get_visualization
from flask import Flask, abort, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    logger.debug("Request for home page.")
    return render_template("home.html")

# TODO:
@app.route("/visualize/<artist>")
@app.route("/visualize/<artist>/<album>")
def visualize(**query):
    logger.debug("Request to visualize <%s>." % repr(query))

    object = music_api.get(query)
    if not object:
        logger.debug("music_api.get() returned False, sending 404.")
        abort(404)

    data = get_visualization(object)

    return render_template(data["template"], **data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Cleaner whitespace in rendered HTML
# TODO: move to configuration file
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

logger = app.logger
music_api = MusicApiWrapper(logger)

if __name__ == '__main__':
   app.run(debug=True)

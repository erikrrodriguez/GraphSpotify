from flask import Flask

app = Flask(__name__)

if not app.debug:
    import logging
    from logging import FileHandler
    from logging import Formatter

    # TODO: fix permissions on this file to be more restrictive..
    file_handler = FileHandler('/var/www/apps/SpotifyGraph/logs/SpotifyGraph.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter('''%(asctime)s %(levelname)s: %(pathname)s:%(lineno)d %(module)s:%(funcName)s %(message)s'''))
    app.logger.addHandler(file_handler)

@app.route("/")
def hello():
    # Only warn or higher work
    app.logger.warn("Testing logging capability.")
    return "Front end of Flask (thus far)"

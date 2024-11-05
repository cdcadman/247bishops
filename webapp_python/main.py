from os import environ
from pathlib import Path

import flask

app = flask.Flask(__name__)

#TODO: Add hash to frontfire download.

@app.before_request
def maintenance_mode():
    if environ["MAINTENANCE_MODE"] == "1":
        return (
            flask.send_file(
                Path(__file__).parent.absolute().parent / "html" / "maintenance.html"
            ),
            503,
        )


@app.route("/")
def main():
    return flask.send_file(
        Path(__file__).parent.absolute().parent / "html" / "main.html"
    )

@app.route("/test")
def main_test():
    return flask.send_file(
        Path(__file__).parent.absolute().parent / "html" / "test.html"
    )

@app.route("/bower_components/<package>/<folder>/<file>")
def bower_component(package, folder, file):
    return flask.send_file(Path(__file__).parent.absolute().parent / "bower_components" / package / folder / file)

@app.route("/favicon.svg")
def favicon():
    """If this is updated, you also need to increment the version in the link tag in the html file.
    See https://stackoverflow.com/questions/2208933/how-do-i-force-a-favicon-refresh"""
    return flask.send_file(
        Path(__file__).parent.absolute().parent / "html" / "Chess_tile_bl.svg"
    )

from pathlib import Path

import flask

app = flask.Flask(__name__)


@app.route("/")
def main():
    return flask.send_file(
        Path(__file__).parent.absolute().parent / "html" / "main.html"
    )


@app.route("/favicon.svg")
def favicon():
    """If this is updated, you also need to increment the version in the link tag in the html file.
    See https://stackoverflow.com/questions/2208933/how-do-i-force-a-favicon-refresh"""
    return flask.send_file(
        Path(__file__).parent.absolute().parent / "html" / "Chess_tile_bl.svg"
    )

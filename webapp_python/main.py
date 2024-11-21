from os import environ
from pathlib import Path

import flask
from werkzeug.exceptions import NotFound

app = flask.Flask(__name__)

RESPONSE_HEADERS = {
    "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; upgrade-insecure-requests",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "X-Content-Type-Options": "nosniff",
}

TOP_LEVEL_PATH = Path(__file__).parent.absolute().parent


@app.before_request
def maintenance_mode():
    if environ["MAINTENANCE_MODE"] == "1" and flask.request.path not in (
        "/favicon.png",
        "/css/main.css",
    ):
        return flask.send_file(TOP_LEVEL_PATH / "html" / "maintenance.html"), 503


@app.after_request
def apply_headers(response):
    for key, val in RESPONSE_HEADERS.items():
        response.headers[key] = val
    return response


@app.route("/")
def main():
    return flask.send_file(TOP_LEVEL_PATH / "html" / "main.html")


@app.route("/favicon.png")
def favicon():
    """If this is updated, you also need to increment the version in the link tag in the html file.
    See https://stackoverflow.com/questions/2208933/how-do-i-force-a-favicon-refresh"""
    return flask.send_file(TOP_LEVEL_PATH / "images" / "247bishops_icon.png")


@app.route("/css/main.css")
def internal_css():
    return flask.send_file(TOP_LEVEL_PATH / "css" / "main.css")


@app.route("/javascript/<file>")
def internal_javascript(file):
    try:
        return flask.send_file(TOP_LEVEL_PATH / "javascript" / file)
    except FileNotFoundError:
        return NotFound()


@app.route("/images/247bishops_symbol.png")
def internal_images():
    return flask.send_file(TOP_LEVEL_PATH / "images" / "247bishops_symbol.png")


@app.route("/front_end_deps/<package>/<file>")
def front_end_deps(package, file):
    try:
        return flask.send_file(TOP_LEVEL_PATH / "front_end_deps" / package / file)
    except FileNotFoundError:
        return NotFound()


# TODO: Tests
# TODO: Add front end installation to workflow.
# TODO: Comment on chess.js in "about".
# TODO: Close issue with PR.
# TODO: Comment about CSP.
# TODO: Add notes to contributing.md

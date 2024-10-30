"""Run this script from python to test the web app locally.
`python run_flask.py` runs it on the default port
`python run_flask.py 5001` runs it on port 5001
Direct your webbrowser to http://127.0.0.1:5001 to view the app (if you ran it on port 5001).
"""
import sys
from app import app

PORT = sys.argv[1] if len(sys.argv) > 1 else 5000

app.run(host="127.0.0.1", port=PORT)

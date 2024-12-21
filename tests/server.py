import signal
import subprocess as sp
import sys
import time
import tomllib
from contextlib import contextmanager
from pathlib import Path

TOML_FILE = Path(__file__).parent.absolute().parent / "pyproject.toml"

WARNING_FILTERS = []
for _filter in tomllib.loads(TOML_FILE.read_text())["tool"]["pytest"]["ini_options"][
    "filterwarnings"
]:
    WARNING_FILTERS.extend(["-W", _filter])

TIMEOUT = 5
PORT = 5000  # this matches the port in the reverse proxy command for Android Virtual Device


def close_server(server: sp.Popen, check_status=True):
    server.send_signal(signal.SIGINT)
    for line in iter(server.stderr.readline, ""):
        sys.stderr.write(line)
    server.stderr.close()
    assert server.wait(TIMEOUT) in (0, -2) or not check_status


@contextmanager
def get_server_url(maintenance_mode: bool = False):
    for _ in range(int(10 * TIMEOUT)):
        server = sp.Popen(
            [sys.executable]
            + WARNING_FILTERS
            + ["run_flask.py", str(PORT), str(maintenance_mode)],
            stderr=sp.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1,
        )
        out = server.stderr.readline()
        sys.stderr.write(out)
        if "Address already in use" in out:
            close_server(server, check_status=False)
            time.sleep(0.1)
        else:
            break
    else:
        raise TimeoutError(f"Could not start a webserver on port {PORT}")
    try:
        yield f"http://127.0.0.1:{PORT}"
    finally:
        close_server(server)

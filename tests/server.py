import signal
import subprocess as sp
import sys
from contextlib import contextmanager

TIMEOUT = 5


def close_server(server: sp.Popen, check_status=True):
    server.send_signal(signal.SIGINT)
    for line in iter(server.stderr.readline, ""):
        sys.stderr.write(line)
    server.stderr.close()
    assert server.wait(TIMEOUT) in (0, -2) or not check_status


@contextmanager
def get_server_url(maintenance_mode: bool = False):
    port = 5000
    while True:
        server = sp.Popen(
            [sys.executable, "run_flask.py", str(port), str(maintenance_mode)],
            stderr=sp.PIPE,
            text=True,
            universal_newlines=True,
            bufsize=1,
        )
        out = server.stderr.readline()
        sys.stderr.write(out)
        if "Address already in use" in out:
            close_server(server, check_status=False)
            port += 1
        else:
            break
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        close_server(server)

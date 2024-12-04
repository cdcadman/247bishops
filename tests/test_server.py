import pytest

from . import server


def test_timeout_error(monkeypatch):
    with server.get_server_url():
        monkeypatch.setattr(server, "TIMEOUT", 0.1)
        with pytest.raises(
            TimeoutError, match=f"Could not start a webserver on port {server.PORT}"
        ):
            with server.get_server_url():
                pass  # pragma: no cover

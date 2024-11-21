import requests

from .server import get_server_url


def test_not_found():
    with get_server_url() as webapp_url:
        response = requests.get(f"{webapp_url}/javascript/not-an-file.js", timeout=30)
        assert response.status_code == 404
        response = requests.get(
            f"{webapp_url}/front_end_deps/not-a-dep/not-a-file.js", timeout=30
        )
        assert response.status_code == 404

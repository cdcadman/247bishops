import requests

from .server import get_server_url


def test_main():
    with get_server_url() as webapp_url:
        response = requests.get(f"{webapp_url}", timeout=60)
        assert response.status_code == 200
        assert "24/7 Bishops" in response.text
        response = requests.get(f"{webapp_url}/favicon.svg?v=1729", timeout=60)
        assert response.status_code == 200

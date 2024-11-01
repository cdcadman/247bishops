import requests

from .server import get_server_url


def test_main():
    with get_server_url() as webapp_url:
        response = requests.get(f"{webapp_url}", timeout=60)
        assert response.status_code == 200
        assert "24/7 Bishops" in response.text
        response = requests.get(f"{webapp_url}/favicon.svg?v=1729", timeout=60)
        assert response.status_code == 200


def test_maint():
    with get_server_url(maintenance_mode=True) as webapp_url:
        response = requests.get(f"{webapp_url}", timeout=60)
        assert response.status_code == 503
        assert "24/7 Bishops is Temporarily Unavailable" in response.text
        response = requests.post(f"{webapp_url}/random_path", timeout=60)
        assert response.status_code == 503
        assert "24/7 Bishops is Temporarily Unavailable" in response.text

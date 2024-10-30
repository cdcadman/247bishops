from .server import get_server_url


def test_port_increment():
    with get_server_url() as first_url:
        first_port = int(first_url.split(":")[2])
        with get_server_url() as second_url:
            second_port = int(second_url.split(":")[2])
            assert second_port > first_port

from pathlib import Path

import pytest
from selenium import webdriver as wd


def chrome():
    options = wd.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=600,1000")
    return wd.Chrome(options=options)


def edge():
    options = wd.EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=600,1000")
    options.add_argument("--force-device-scale-factor=1.25")
    options.add_argument("--device-scale-factor=1.25")
    return wd.Edge(options=options)


def firefox():
    options = wd.FirefoxOptions()
    options.add_argument("-headless")
    kwargs = {"options": options}
    executable_path = "/snap/bin/geckodriver"
    if Path(executable_path).exists():  # pragma: no cover
        service = wd.FirefoxService(executable_path=executable_path)
        kwargs["service"] = service
    return wd.Firefox(**kwargs)


@pytest.fixture(params=[chrome, edge, firefox])
def driver(request):
    with request.param() as _driver:
        yield _driver

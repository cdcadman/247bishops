import pytest
from selenium import webdriver as wd


def chrome():
    options = wd.ChromeOptions()
    options.add_argument("--headless=new")
    return wd.Chrome(options=options)


def edge():
    options = wd.EdgeOptions()
    options.add_argument("--headless=new")
    return wd.Edge(options=options)


def firefox():
    options = wd.FirefoxOptions()
    options.add_argument("-headless")
    return wd.Firefox(options=options)


@pytest.fixture(params=[chrome, edge, firefox])
def driver(request):
    with request.param() as _driver:
        yield _driver

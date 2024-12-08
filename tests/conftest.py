import pytest
from selenium import webdriver as wd

ALL_BROWSERS = []


def browser(func):
    ALL_BROWSERS.append(func)
    return func


@browser
def chrome():
    options = wd.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=600,1000")
    return wd.Chrome(options=options)


@pytest.fixture(params=ALL_BROWSERS)
def driver(request):
    with request.param() as _driver:
        yield _driver

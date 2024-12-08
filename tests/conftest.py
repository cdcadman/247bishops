from pathlib import Path

import pytest
from appium.options.android import UiAutomator2Options
from appium.webdriver import Remote
from appium.webdriver.appium_connection import AppiumConnection
from selenium import webdriver as wd
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.client_config import ClientConfig
from urllib3.exceptions import ReadTimeoutError

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


@browser
def edge():
    options = wd.EdgeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=600,1000")
    options.add_argument("--force-device-scale-factor=1.25")
    options.add_argument("--device-scale-factor=1.25")
    webdriver = wd.Edge(options=options)
    _exc = None
    for _ in range(5):
        try:
            webdriver.get("https:/www.google.com")
        except ReadTimeoutError as exc:  # pragma: no cover
            _exc = exc
        else:
            return webdriver
    raise _exc  # pragma: no cover


@browser
def firefox():
    options = wd.FirefoxOptions()
    options.add_argument("-headless")
    kwargs = {"options": options}
    executable_path = "/snap/bin/geckodriver"
    if Path(executable_path).exists():  # pragma: no cover
        service = wd.FirefoxService(executable_path=executable_path)
        kwargs["service"] = service
    return wd.Firefox(**kwargs)


@browser
def android_chrome():
    capabilities = dict(
        platformName="Android",
        browserName="chrome",
        uiautomator2ServerLaunchTimeout=60000,
    )
    appium_server_url = "http://localhost:4723"
    client_config = ClientConfig(appium_server_url)
    command_executor = AppiumConnection(client_config=client_config)
    options = UiAutomator2Options()
    options.load_capabilities(capabilities)
    _exc = None
    for _ in range(5):
        try:
            return Remote(command_executor, options=options)
        except WebDriverException as exc:  # pragma: no cover
            _exc = exc
    raise _exc  # pragma: no cover


@pytest.fixture(params=ALL_BROWSERS)
def driver(request):
    with request.param() as _driver:
        yield _driver

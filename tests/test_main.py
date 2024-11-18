from selenium.webdriver.remote.webdriver import BaseWebDriver

from .server import get_server_url


def test_main(driver: BaseWebDriver):
    with get_server_url() as webapp_url:
        driver.get(webapp_url)


def test_maint(driver: BaseWebDriver):
    with get_server_url(maintenance_mode=True) as webapp_url:
        driver.get(webapp_url)

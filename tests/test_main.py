from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .server import get_server_url

TIMEOUT = 5


def test_main(driver: BaseWebDriver):
    with get_server_url() as webapp_url:
        driver.get(webapp_url)
        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "about"))
        )
        about = driver.find_element(By.ID, "about")
        assert about.get_attribute("innerText") == "About 24/7 Bishops"
        about_popup = driver.find_element(By.ID, "about_popup")
        assert not about_popup.is_displayed()
        about.click()
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "about_popup"))
        )
        assert "GNU Affero General Public License" in driver.find_element(
            By.ID, "about_popup"
        ).get_attribute("innerText")
        assert about_popup.is_displayed()
        driver.find_element(By.ID, "close_about_popup").click()
        WebDriverWait(driver, TIMEOUT).until(lambda d: not about_popup.is_displayed())


def test_maint(driver: BaseWebDriver):
    with get_server_url(maintenance_mode=True) as webapp_url:
        driver.get(webapp_url)
        WebDriverWait(driver, TIMEOUT).until(
            EC.text_to_be_present_in_element(
                (By.TAG_NAME, "h1"), "24/7 Bishops is Temporarily Unavailable"
            )
        )

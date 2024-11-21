from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .server import get_server_url

TIMEOUT = 5


def click(driver: BaseWebDriver, square: str):
    row = 8 - int(square[1])
    column = ord(square[0]) - 97
    canvas = driver.find_element(By.ID, "work_board_canvas")
    rect = canvas.rect
    assert rect["height"] == rect["width"]
    scale_factor = rect["height"] / 256
    ActionChains(driver).move_to_element_with_offset(
        canvas,
        scale_factor * (16 + column * 32 - 136),
        scale_factor * (16 + row * 32 - 136),
    ).click().perform()

def click_multiple(driver: BaseWebDriver, squares: list[str], check_move_list: str):
    for square in squares:
        click(driver, square)
    move_list = driver.find_element(By.ID, "move_list")
    assert move_list.get_attribute("innerHTML") == check_move_list

def test_work_board(driver: BaseWebDriver):
    with get_server_url() as webapp_url:
        driver.get(webapp_url)
        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "work_board"))
        )
        driver.find_element(By.ID, "work_board").click()
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "work_board_canvas"))
        )
        move_list = driver.find_element(By.ID, "move_list")
        click_multiple(driver, ["e2", "e4"], "1. e4")
        click_multiple(driver, ["e4", "e2"], "1. e4")
        click_multiple(driver, ["e7", "e5"], "1. e4 e5")
        driver.find_element(By.ID, "work_board_back").click()
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: move_list.get_attribute("innerHTML") == "1. e4")
        click_multiple(driver, ["e7", "e5"], "1. e4 e5")
        click_multiple(driver, ["f2", "f4"], "1. e4 e5 2. f4")
        click_multiple(driver, ["f7", "f5"], "1. e4 e5 2. f4 f5")
        click_multiple(driver, ["e4", "f5"], "1. e4 e5 2. f4 f5 3. exf5")
        click_multiple(driver, ["e5", "f4"], "1. e4 e5 2. f4 f5 3. exf5 exf4")
        click_multiple(driver, ["f5", "f6"], "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6")
        click_multiple(driver, ["f4", "f3"], "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6 f3")
        click_multiple(driver, ["f6", "g7"], "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6 f3 5. fxg7")
        click_multiple(driver, ["f3", "g2"], "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6 f3 5. fxg7 fxg2")
        click(driver, "g7")
        click(driver, "h8")
        alert = driver.switch_to.alert
        assert alert.text == "Promotion piece (q, r, b, or n)?"
        alert.send_keys("q")
        alert.accept()
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: move_list.get_attribute("innerHTML") == "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6 f3 5. fxg7 fxg2 6. gxh8=Q")
        click(driver, "g2")
        click(driver, "h1")
        alert = driver.switch_to.alert
        assert alert.text == "Promotion piece (q, r, b, or n)?"
        alert.send_keys("n")
        alert.accept()
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: move_list.get_attribute("innerHTML") == "1. e4 e5 2. f4 f5 3. exf5 exf4 4. f6 f3 5. fxg7 fxg2 6. gxh8=Q gxh1=N")

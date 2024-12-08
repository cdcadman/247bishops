from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .server import get_server_url

TIMEOUT = 5


def get_element(driver: BaseWebDriver, square: str):
    if square is None:
        return driver.find_element(By.XPATH, "//*[@id='move_list']")
    row = 8 - int(square[1])
    column = ord(square[0]) - 97
    return driver.find_element(By.XPATH, f"//*[@id='work_board_{8*row+column}']")


def make_move(
    driver: BaseWebDriver,
    from_square: str,
    to_square: str = None,
    move_list_append: str = "",
    promotion_piece=None,
):
    move_list = driver.find_element(By.XPATH, "//*[@id='move_list']")
    orig_move_list = move_list.text
    from_elmt = get_element(driver, from_square)
    to_elmt = get_element(driver, to_square)
    ActionChains(driver).drag_and_drop(from_elmt, to_elmt).perform()
    if promotion_piece is not None:
        alert = driver.switch_to.alert
        assert alert.text == "Promotion piece (q, r, b, or n)?"
        alert.send_keys(promotion_piece)
        alert.accept()
    assert move_list.text == orig_move_list + move_list_append


def test_work_board(driver: BaseWebDriver):
    with get_server_url() as webapp_url:
        driver.get(webapp_url)
        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='work_board']"))
        )
        driver.find_element(By.XPATH, "//*[@id='work_board']").click()
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='work_board_table']"))
        )
        make_move(driver, "e2", "e4", "1. e4")
        make_move(driver, "e7", "d6")  # Illegal move
        make_move(driver, "e7", "e5", " e5")
        make_move(driver, "f2", "f4", " 2. f4")
        make_move(driver, "f7", "f5", " f5")
        make_move(driver, "e4")  # checks dragging off the board is ok.
        make_move(driver, "e4", "f5", " 3. exf5")
        make_move(driver, "e5", "f4", " exf4")
        make_move(driver, "f5", "f6", " 4. f6")
        make_move(driver, "f4", "f3", " f3")
        make_move(driver, "f6", "g7", " 5. fxg7")
        make_move(driver, "f3", "g2", " fxg2")
        make_move(driver, "g7", "f8", " 6. gxf8=N", "n")
        make_move(driver, "g2", "f1", " gxf1=Q+", "q")
        driver.find_element(By.XPATH, "//*[@id='work_board_back']").click()
        move_list = driver.find_element(By.XPATH, "//*[@id='move_list']")
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: move_list.text.endswith("6. gxf8=N")
        )

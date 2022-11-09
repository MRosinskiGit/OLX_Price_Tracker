# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to find everywhere for classes, files, tool windows, actions, and settings.
import time

from log_print import Log
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Ofert:
    def __init__(self, olxofert: WebElement):
        self.price = olxofert.find_element(by=By.CLASS_NAME, value="price").text
        self.name = olxofert.find_element(by=By.CLASS_NAME, value="normal").text
        self.link = olxofert.find_element(by=By.XPATH, value="//*[contains(@class,'offerLink')]").get_attribute("href")
        self.link = self.link[:self.link.find(".html") + 5]
        self.date_n_location = olxofert.find_element(by=By.CLASS_NAME, value="date-location").text


def read_fav_oferts(driver, _mail: str, _password: str) -> list:
    """

    :param driver:
    :param _mail:
    :param _password: 
    :return: 
    """

    Log("Open selenium web")
    driver.implicitly_wait(15)

    Log("Load olx")
    driver.get("https://www.olx.pl/")
    driver.implicitly_wait(5)

    Log("Accept cookies")
    driver.find_element(by=By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]').click()

    Log("Log in")
    driver.find_element(by=By.XPATH, value='//*[@id="topLoginLink"]').click()
    driver.find_element(by=By.NAME, value='username').send_keys(_mail)
    driver.find_element(by=By.NAME, value='password').send_keys(_password)
    driver.find_element(by=By.XPATH, value='//*[@data-testid="login-submit-button"]').click()

    Log("Close popup")
    for _ in range(3):
        try:
            close_button = driver.find_element(by=By.XPATH, value='//*[@aria-label="Close"]')
            close_button.click()
            break
        except NoSuchElementException as error:
            time.sleep(1)
            Log(str(error))

    Log("Go to fav tab")
    driver.get("https://www.olx.pl/obserwowane/")
    for _ in range(2):
        try:
            change_view_button = driver.find_element(by=By.XPATH, value='//*[@id="observedViewTiles"]')
            change_view_button.click()
            break
        except NoSuchElementException as error:
            time.sleep(1)
            Log(str(error))

    Log("Get WebObject and extract data")

    for _ in range(3):
        oferts_data = []
        try:
            oferts = driver.find_elements(by=By.XPATH, value="//*[contains(@class,'observedad')]")
            for element in oferts:
                oferts_data.append(Ofert(element))
            break
        except (NoSuchElementException, StaleElementReferenceException) as error:
            time.sleep(1)
            Log(str(error))

    return oferts_data

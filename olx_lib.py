import time

from datetime import datetime
from dicts.months import months
from log_print import Log
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Offer:
    def __init__(self, olx_offer: WebElement):
        self.price = olx_offer.find_element(by=By.CLASS_NAME, value="price").text
        self.name = olx_offer.find_element(by=By.CLASS_NAME, value="normal").text
        self.link = olx_offer.find_element(by=By.XPATH, value=".//*[contains(@class,'offerLink')]").get_attribute(
            "href")
        self.link = self.link[:self.link.find(".html") + 5]
        date_n_location = olx_offer.find_element(by=By.CLASS_NAME, value="date-location").text
        self.extract_date_n_location(date_n_location)

    def extract_date_n_location(self, date_n_location):
        if 'dzisiaj' in date_n_location:
            self.location = date_n_location[:date_n_location.find("dzisiaj") - 1]
            self.date = datetime.now().strftime('%d/%m/%Y')
        else:
            for i in date_n_location:
                if not i.isdigit():
                    pass
                else:
                    cut_pointer = date_n_location.index(i)
                    break
            self.location = date_n_location[:cut_pointer - 1]
            date_n_location = date_n_location[cut_pointer:]
            for i in date_n_location:
                if not i.isdigit():
                    cut_pointer = date_n_location.index(i)
                    break
            try:
                self.date = f"{date_n_location[:cut_pointer]}/{months[date_n_location[cut_pointer + 1:]]}/{datetime.now().strftime('%Y')[2:]}"
            except KeyError:
                self.date = f"{date_n_location[:cut_pointer]}/{date_n_location[cut_pointer + 1:]}/{datetime.now().strftime('%Y')[2:]}"


def read_fav_oferts(driver, _mail: str, _password: str) -> list[Offer]:
    """

    :param driver:
    :param _mail:
    :param _password:
    :return: list
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
    time.sleep(1)
    for _ in range(2):
        try:
            change_view_button = driver.find_element(by=By.XPATH, value='//*[@id="observedViewTiles"]')
            change_view_button.click()
            break
        except NoSuchElementException as error:
            time.sleep(1)
            Log(str(error))

    Log("Get WebObject and extract data")
    time.sleep(1)
    for _ in range(3):
        offers_data = []
        try:
            oferts = driver.find_elements(by=By.XPATH, value="//*[contains(@class,'observedad')]")
            for element in oferts:
                offers_data.append(Offer(element))
            break
        except (NoSuchElementException, StaleElementReferenceException) as error:
            time.sleep(1)
            Log(str(error))

    return offers_data

from olx_lib import read_fav_oferts
from selenium import webdriver

if __name__ == "__main__":
    with open('password.txt', 'r') as file:
        password = file.read()

    driver = webdriver.Chrome()

    oferts = read_fav_oferts(driver=driver, _mail='m.rosinski97@gmail.com', _password=password)

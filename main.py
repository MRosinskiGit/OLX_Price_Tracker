from excel_olx import Offersheet
from olx_lib import read_fav_oferts
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

EXCEL_FILE_NAME = "oferts.xlsx"

if __name__ == "__main__":
    with open('config.conf', 'r') as file:
        data = file.readlines()
        password = data[1].replace("password:", "")
        email = data[0].replace("email:", "").replace("\n", "")

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    offers = read_fav_oferts(driver=driver, _mail=email, _password=password)

    driver.quit()

    excel_sheet = Offersheet(EXCEL_FILE_NAME)

    excel_sheet.search_inactive_offers(offers)

    for offer in offers:
        offer_row = excel_sheet.look_for_value(search_by_category="Link", value=offer.link)
        if offer_row is None:
            inactive_row = excel_sheet.look_in_inactive(search_by_category="Name", value=offer.name)
            if inactive_row is None:
                excel_sheet.add_new_offer(offer=offer)
            else:
                new_row = excel_sheet.move_row(frm=inactive_row, to=excel_sheet.find_first_empty_row())
                excel_sheet.compare_offers(new_row, offer)
        else:
            excel_sheet.compare_offers(offer_row, offer)
    excel_sheet.save_file()

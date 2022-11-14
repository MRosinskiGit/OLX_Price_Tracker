from excel_olx import Offersheet
from olx_lib import read_fav_oferts
from selenium import webdriver

EXCEL_FILE_NAME = 'test.xlsx'
# offers = [Offer("6 500 zł","www.onet.pl"), Offer("19 999 zł", "www.wp.pl")]


if __name__ == "__main__":
    with open('password.txt', 'r') as file:
        password = file.read()
        #change to config file

    driver = webdriver.Chrome()
    offers = read_fav_oferts(driver=driver, _mail='m.rosinski97@gmail.com', _password=password)
    #todo change email reading
    driver.close()

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

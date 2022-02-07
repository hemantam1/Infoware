from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup
import datetime
import time
import csv
import pandas as pd

options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2,
	"profile.managed_default_content_settings.images": 2}
#options.add_argument("--headless")
options.add_experimental_option("prefs",prefs)
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--incognito")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
url = 'https://www.dmart.in/'
headers = ['Name', 'MRP', 'Price', 'Pincode']
count = 0

#Function to open the respective pincode page.
def dm_pinc(p: int):
    time.sleep(1)
    try:
        driver.find_element_by_class_name("src-client-components-header-__header-module___pincode").click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="pincodeInput"]').clear()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="pincodeInput"]').send_keys(p)
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/ul/li/button').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button').click()
        driver.implicitly_wait(2)
    except:
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="pincodeInput"]').clear()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="pincodeInput"]').send_keys(p)
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/ul/li/button').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button').click()
        driver.implicitly_wait(2)
    time.sleep(1)

#Function to generate the links for the products to make it easier to run.
def dm_links(products: list):
    links = []
    for i in products['dmart']:
        if i != "None":
            links.append('https://www.dmart.in/product/{}/'.format(i))
    return links

#Function to navigate the product list through the pincodes and scrap the required data.
def dm_items_scraper(link, pincode):
    info = []
    driver.execute_script("window.open('{}', '_blank')".format(link))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    Title = soup.find('div', class_='src-client-app-product-details-styles-__text-label-component-module___title-container')
    t = Title.text.strip() if Title else 'None'
    MRP = soup.find('span',class_='src-client-app-product-details-styles-__price-details-component-module___mrp')
    m = MRP.text.strip().split(u'\u20B9')[1] if MRP else 'None'
    Price = soup.find("span",class_='src-client-app-product-details-styles-__price-details-component-module___sp')
    p = Price.text.strip().split(u'\u20B9')[1] if Price else 'None'

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    if t != 'None': 
        info.append((t, m, p, pincode)) 
    return info
    
#Main function to execute all the functions.
if __name__ == "__main__":
    start = datetime.datetime.now()
    driver.get(url)
    products = pd.read_csv("Generated_Files/items.csv")
    pincodes_df = pd.read_excel('Generated_Files/pincodes/pincodes_dmart.xlsx')
    links = dm_links(products)
    with open('Generated_Files/Scrapped_Files/dmart_scraper.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for pin in pincodes_df['Pin Code']:
            dm_pinc(pin)
            for li in links:
                count += 1
                items = dm_items_scraper(li, pin)
                for i in items:
                    csvwriter.writerow({'Name':i[0], 'MRP':i[1], 'Price':i[2], 'Pincode': i[3]})
                    print("%s -- "%count+"Name: {}, MRP: {}, Price: {}, Pincode: {}".format(i[0], i[1], i[2], i[3]))
    end = datetime.datetime.now()
    print(end - start)
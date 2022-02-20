from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import datetime
import warnings

warnings.filterwarnings('ignore')

pincodes_df = pd.read_excel('Required files/pincodes.xlsx')
options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2,
	"profile.managed_default_content_settings.images": 2,}
options.add_experimental_option("prefs",prefs)
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--incognito")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
url = 'https://www.amazon.in/'
headers = ['ASIN', 'Name', 'MRP', 'Price', 'Pincode']
info = []
count = 0

#Function to open the respective pincode page.
def az_pinc(p: int) -> int:
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="nav-global-location-popover-link"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').clear()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(p)
        driver.implicitly_wait(5)
    except ElementClickInterceptedException:
        driver.refresh()
        driver.find_element_by_xpath('//*[@id="nav-global-location-popover-link"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').clear()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(p)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipInputSection"]').send_keys(Keys.ENTER)

    driver.find_element_by_xpath('//*[@id="GLUXZipInputSection"]/div[2]').click()
    driver.implicitly_wait(5)
    time.sleep(5)

#Function to generate the links for the products to make it easier to run.
def az_links(products: list) -> list:
    links = []
    for i in products['ASIN']:
        links.append('https:/www.amazon.in/dp/{}/'.format(i))
    return links

#Function to navigate the product list through the pincodes and scrap the required data.
def az_items_scraper(links: list, products: list, count: int, pincodes: list):
    for pin in pincodes[:5]:
        az_pinc(pin)
        for ASIN, link in zip(products['ASIN'], links):
            driver.execute_script("window.open('{}', '_blank')".format(link))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            ASIN = ASIN
            Title = soup.find('span', {'id' : 'productTitle'})
            t = Title.text.strip() if Title else 'None' 
            MRP = soup.find('span', {'class': 'priceBlockStrikePriceString a-text-strike'})
            m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None' 
            try:
                Price = soup.find('span', {'id': 'priceblock_ourprice'})
            except:    
                Price = soup.find('span', {'id':'priceblock_dealprice'})
            p = Price.text.strip().split('\u20b9')[1] if Price else 'None'
            pc = soup.find('span', {'class':'nav-line-2 nav-progressive-content'})
            pinco = pc.text.strip() if pc else 'None'
            if t != 'None': info.append((ASIN, t, m, p, pin)) 
            print("%s -- "%count+"ASIN: {}, Name: {}, MRP: {}, Price: {}, Pincode: {}".format(ASIN, t, m, p, pinco))
            
            count += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    return info

#Main function to execute all the functions.
if __name__ == '__main__':
    start = datetime.datetime.now()
    products = pd.read_csv("Required files/items.csv")
    l = az_links(products[:5])
    driver.get(url)
    #Using CSV library to write the scrapped details to a .csv file.
    with open('Scrapped_Files/amazon-products.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        items = az_items_scraper(l, products, count, pincodes_df['Pin Code'])
        for i in items:
            csvwriter.writerow({'ASIN':i[0], 'Name':i[1], 'MRP':i[2], 'Price':i[3], 'Pincode': i[4]})
    end = datetime.datetime.now()
    print(end - start)
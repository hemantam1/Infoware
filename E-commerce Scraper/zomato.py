from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import datetime
import re

options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2,
	"profile.managed_default_content_settings.images": 2,}
options.add_experimental_option("prefs",prefs)
#options.add_argument("--headless")
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--incognito")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
#url = 'https://www.zomato.com/'
headers = ['Name', 'Price', 'Description', 'Rating']
time.sleep(5)
pincodes = pd.read_excel('Generated_Files/pincodes_zomato.xlsx')

def z_pincodes(city):
    driver.execute_script("window.open('{}{}', '_blank')".format(url, city))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    
    print("{}{}".format(url, city))
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def z_scraper(source):
    items = []
    dish = source.find_all('div', {'class':'sc-1s0saks-17 bGrnCu'})
    for d in dish:
        name = d.find('h4', {'class':'sc-1s0saks-15 iSmBPS'})
        d_name = name.text.strip() if name else 'None'
        price = d.find('span', {'class':'sc-17hyc2s-1 cCiQWA'})
        d_price = price.text.strip().split('\u20b9')[1] if price else 'None'
        description = d.find('p', {'class':'sc-1s0saks-12 hcROsL'})
        d_description = description.text.strip() if description else "None"
        rating = d.find('span', {'class':'sc-z30xqq-4 hTgtKb'})
        d_rating = rating.text.strip() if rating else 'None'
        if d_name != 'None':
            items.append((d_name, d_price, d_rating, d_description))
    return items

def z_read_more(list_read_more):
    for a in list_read_more:
        a.click()
        driver.implicitly_wait(2)

if __name__ == "__main__":
    url = "https://www.zomato.com/ahmedabad/la-pinoz-pizza-1-naranpura/order"
    driver.get(url)
    read_more = driver.find_elements_by_xpath("//./span[@class='sc-ya2zuu-0 SWRrQ']")
    z_read_more(read_more)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info = z_scraper(soup)
    count = 0
    with open('Generated_Files/zomato_la-pinoz.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for i in info:
            csvwriter.writerow({'Name': i[0], 'Price': i[1], 'Description': i[3], 'Rating': i[2]})
            print('%s -- '%count+'Name: {}, Price: {}, Description: {}, Rating: {}'.format(i[0], i[1], i[3], i[2]))


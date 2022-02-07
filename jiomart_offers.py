from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import datetime
import re

options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2,
	"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs",prefs)
#options.add_argument('--headless')
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--incognito")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
headers = ['JIO', 'Name', 'MRP', 'Price', 'Link']
url = 'https://www.jiomart.com/c/groceries/bestdeals/bestival-edition-2-main-sale/2978?prod_mart_groceries_products_popularity%5BrefinementList%5D%5Bin_stock%5D%5B0%5D=1&prod_mart_groceries_products_popularity%5Bpage%5D=20'
info = []
count = 0

def jio_links(driver):
    info = []
    objects = driver.find_elements_by_xpath('//./a[@class="category_name prod-name"]')
    for obj in objects:
        info.append(obj.get_attribute('href'))
    return info

def jio_item_scraper(link):
    infor = []
    driver.execute_script("window.open('{}', '_blank')".format(link))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jio = re.findall(r"(?<=/)[0-9]{9}", link)
    Title = soup.find('div', class_='title-section')
    t = Title.text.strip() if Title else 'None'
    MRP = soup.find('span',class_='price')
    m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
    Price = soup.find('span',class_='final-price')
    p = Price.text.strip().split('\u20b9')[1] if Price else 'None'
    infor.append((jio, t, m, p, link)) 
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return infor

if __name__ == '__main__':
    start = datetime.datetime.now()
    driver.get(url)
    time.sleep(3)
    for i in range(0,20):
        if driver.find_element_by_class_name('ais-InfiniteHits-loadMore'):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        else:
            break
    links = jio_links(driver)
    count = 0
    with open('Generated_Files/Scrapped_Files/jiomart-offers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for li in links:
            count += 1
            information = jio_item_scraper(li)
            for i in information:
                print("{} --, JIO: {}, Name: {}, MRP: {}, Price: {}, Link: {}".format(count, i[0], i[1], i[2], i[3], i[4]))
                csvwriter.writerow({'JIO': i[0], 'Name': i[1], 'MRP': i[2], 'Price': i[3], 'Link': i[4]})
    end = datetime.datetime.now()
    print(end - start)

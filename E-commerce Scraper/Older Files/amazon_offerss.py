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

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
url = 'https://www.amazon.in/gp/goldbox?ref_=nav_cs_gb_5bf06ae8328043a2beb2754f40a54c84'
headers = ['ASIN', 'Pincode', 'Name', 'MRP', 'Price', 'Link']
count = 0

def az_card_holder(driver):
    links = []
    #objects = driver.find_elements_by_xpath("//./a[@class='a-link-normal  a-color-base a-text-normal']")
    objects = driver.find_elements_by_xpath("//./a[@class='a-link-normal']")
    for link in objects:
        links.append((link.text.strip(), link.get_attribute('href')))
    return links
#counter = 0
def az_links(webpage):
    links = []
    if re.findall(r"(?<=dp/)[A-Z0-9]{10}", webpage):
        #print("{}-{}".format(counter, webpage))
        links.append(webpage)
    else:
        driver.execute_script("window.open('{}', '_blank')".format(webpage))
        driver.switch_to.window(driver.window_handles[1])
        #print("{}-{}".format(counter, webpage))
        time.sleep(2)
        objects = driver.find_elements_by_xpath('//./span/div/div[2]/div[2]/a') or driver.find_elements_by_xpath("//div[@class='a-section a-spacing-none']/div/h2/a") or driver.find_elements_by_xpath("//./span/div/div[2]/div[1]/a")
        #count = 0
        for link in objects:
            #count += 1
            #print("   {}-{}".format(count, link.get_attribute('href')))
            links.append(link.get_attribute('href'))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return links

def az_item_scraper(page, count):
    info = []
    driver.execute_script("window.open('{}', '_blank')".format(page))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    count += 1
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ASIN = re.findall(r"(?<=dp/)[A-Z0-9]{10}", page)
    a = ASIN[0] if ASIN else 'None'
    Title = soup.find('span', {'id' : 'productTitle'})
    t = Title.text.strip() if Title else 'None' 
    MRP = soup.find('span', {'class': 'priceBlockStrikePriceString a-text-strike'})
    m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
    Price = soup.find('span', {'id': 'priceblock_dealprice'}) or soup.find('span', {'id':'priceblock_ourprice'})
    try:
        if Price.text.strip().replace('\u20b9', ''):
            p = Price.text.strip().replace('\u20b9', '')
        elif Price.text.strip().replace('\u0394', ''):
            p = Price.text.strip().replace('\u0394', '')
        elif Price.text.strip().replace('\u2011', ''):
            p = Price.text.strip().replace('\u2011', '')
    except:
        if not Price: p = 'None'
    pc = soup.find('span', {'class':'nav-line-2 nav-progressive-content'})
    pinco = pc.text.strip() if pc else 'None'
    if t != "None":
        info.append((a, pinco, t, m, p, page)) 
    print("%s -- "%count+"ASIN: {}, Pincode: {}, Name: {}, MRP: {}, Price: {}, Link: {}".format(a, pinco, t, m, p, page))

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    return info

if __name__ == '__main__':
    start = datetime.datetime.now()
    driver.get(url)
    links = []
    link = az_card_holder(driver)
    with open('Scrapped_Files/amazon-offers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for li in link:
            count += 1
            #print("{} -- Name: {}, Link: {}".format(count, li[0], li[1]))
            product_links = az_links(li[1])
            count = 0
            for product in product_links[:10]:
                information = az_item_scraper(product, count)
                for i in information:
                    csvwriter.writerow({'ASIN': i[0], 'Pincode': i[1], 'Name': i[2], 'MRP': i[3], 'Price': i[4], 'Link': i[5]})
    end = datetime.datetime.now()
    print(end - start)

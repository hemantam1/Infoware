import pandas as pd
from amazon_offers_functions import *
from selenium import webdriver
import csv
import datetime
import warnings

warnings.filterwarnings('ignore')

options = Options()
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--incognito")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

url = 'https://www.amazon.in/'
headers = ['ASIN', 'Name', 'MRP', 'Price', 'Pincode']
driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)

pincodes_df = pd.read_excel('Required files/pincodes.xlsx')
products = pd.read_csv("Required files/items.csv")['ASIN']
links = amz_links_generator(products)

with open('Scrapped_Files/amazon-products-test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()
    for p in pincodes_df['Pin Code'][:5]:
        driver.get(url)
        amz_pincode(p, driver)
        for link in links:
            amz_details_scraper(link[:5], csvwriter)
        driver.close()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import datetime
import warnings

warnings.filterwarnings('ignore')
start = datetime.datetime.now()

options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2,
	"profile.managed_default_content_settings.images": 2}
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
url = 'https://grofers.com/'
driver.get(url)
headers = ['Grofers', 'Name', 'Pincode', 'MRP', 'Price']
count = 0

def g_pincodes(city):
    try:
        driver.find_element(By.CLASS_NAME, 'Select-placeholder').click().send_keys(city)
        driver.implicitly_wait(3)
    except:
        driver.refresh()
        driver.find_element(By.CLASS_NAME, 'Select-placeholder').click().send_keys(city)
        driver.implicitly_wait(3)

def g_product_scraper(count, id):
    info = []
    name = products['Name'][count].replace(' ', '-')
    driver.implicitly_wait(2)
    driver.execute_script("window.open('https://grofers.com/prn/{}/prid/{}', '_blank')".format(name, id))
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    grofer = i
    Title = soup.find('h1', class_='pdp-product__name')
    t = Title.text.strip() if Title else 'None'
    #pincode = soup.find('div', class_='user-address')
    pin = pincode.text.strip() if pincode else 'None' 
    MRP = soup.find('span',class_="pdp-product__price--old")
    m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
    Price = soup.find('span',class_='pdp-product__price--new')
    p = Price.text.strip().split('\u20b9')[1] if Price else 'None'
    
    if t: info.append((grofer, t, pin, m, p))
    print("%s -- "%count+"Grofer: {}, Name: {}, Pincode: {}, MRP: {}, Price: {}".format(grofer, pin, t, m, p))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return info

if __name__ == "__main__":
    products = pd.read_csv("Required Files\items.csv")
    pincodes_df = pd.read_csv('Required files\pincodes_grofers.xlsx')
    with open('Scrapped_Files/grofer-products.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for pincode in pincodes_df['City']:
            g_pincodes(pincode)
            for i in products['Grofers']:
                if i != 'None':
                    inf = g_product_scraper(count, i)
                else:
                    grofer = 'None'
                    t = products['Name'][count]
                    m = p = 'None'
                for i in inf:
                    csvwriter.writerow({'Grofers':i[0], 'Pincode': i[1], 'Name':i[2], 'MRP':i[3], 'Price':i[4]})
                count += 1
            driver.close()
    end = datetime.datetime.now()
    print(end - start)
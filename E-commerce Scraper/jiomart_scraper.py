from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import datetime

pincodes_df = pd.read_excel('Generated_Files/pincodes/pincodes_jiomart.xlsx')
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
url = 'https://www.jiomart.com/'
headers = ['JIO', 'Name', 'MRP', 'Price', 'Pincode']
info = []
count = 0

#Function to open the respective pincode page.
def jio_pinc(p: int):
    driver.find_element_by_xpath('//*[@id="pincode_section"]/div[1]').click()
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="rel_pincode"]').clear()
    driver.find_element_by_xpath('//*[@id="rel_pincode"]').send_keys(p)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//*[@id="rel_pincode_form"]/div[1]/button[2]').click()
    driver.implicitly_wait(3)

#Function to generate the links for the products to make it easier to run.
def jio_links(products: list):
    links = []
    jio = []
    na = 'p'
    for i in products['jio']:
        if i != 'None':
            jio.append(i)
            links.append('https://www.jiomart.com/p/groceries/{}/{}'.format(na, i))
    return links, jio

#Function to navigate the product list through the pincodes and scrap the required data.
def jio_items_scraper(links: list, id: int, count: int, pincodes: list):
    for pin in pincodes:
        jio_pinc(pin)
        item = 0
        flag = 0
        for jio, link in zip(id, links):
            driver.execute_script("window.open('{}', '_blank')".format(link))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            jio = jio
            Title = soup.find('div', class_='title-section')
            t = Title.text.strip() if Title else 'None'
            MRP = soup.find('span',class_='price')
            m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
            Price = soup.find('span',class_='final-price')
            p = Price.text.strip().split('\u20b9')[1] if Price else 'None'
            if t != "None":
                info.append((jio, t, m, p, pin)) 
            else:
                flag += 1
            count += 1
            item += 1
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    return info

#Main function to execute all the functions.
if __name__ == "__main__":
    start = datetime.datetime.now()
    products = pd.read_csv("Generated_Files/items.csv")
    l, id = jio_links(products)
    driver.get(url)
    #Using CSV library to write the scrapped details to a .csv file.
    with open('Generated_Files/Scrapped_Files/jiomart_scraper.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        items = jio_items_scraper(l, id, count, pincodes_df['Pin Code'])
        for i in items:
            print('JIO: {}, Name: {}, MRP: {}, Price: {}, Pincode: {}'.format(i[0], i[1], i[2], i[3], i[4]))
            csvwriter.writerow({'JIO':i[0], 'Name':i[1], 'MRP':i[2], 'Price':i[3], 'Pincode': i[4]})
    end = datetime.datetime.now()
    print(end - start)

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
url = 'https://www.bigbasket.com/'
headers = ['EAN', 'Name', 'MRP', 'Price', 'Pincode/City']
info = []
count = 0

#Function to open the respective pincode page.
def bb_pinc(p: int, c: str):
    time.sleep(2)
    try:
        driver.find_element_by_class_name('hvc').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[1]/div/div/span/span[2]/span').click() #dropdown list
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[1]/div/input[1]').send_keys(c, Keys.ENTER)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="areaselect"]').clear()
        driver.find_element_by_xpath('//*[@id="areaselect"]').send_keys(p, Keys.ENTER)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[3]/button').click()
        driver.implicitly_wait(5)
    except NoSuchElementException or ElementClickInterceptedException:
        
        driver.refresh()
        driver.find_element_by_class_name('Input-tvw4mq-0 AddressDropdown___StyledInput-i4k67t-5 wCGnK gkTwgv').click()
        driver.implicitly_wait(5)
        driver.find_element_by_class_name('Input-tvw4mq-0 AddressDropdown___StyledInput-i4k67t-5 wCGnK gkTwgv').send_keys(c)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('AddressDropdown___StyledMenuItem-i4k67t-6 gPWTKH').click()
        driver.implicitly_wait(5)
    time.sleep(5)

#Function to generate the links for the products to make it easier to run.
def bb_links(products: list):
    links = []
    for i in products['EAN']:
        links.append('https://www.bigbasket.com/pd/{}/'.format(i))
    return links

#Function to navigate the product list through the pincodes and scrap the required data.
def bb_items_scraper(links: list, products: list, count: int, pincodes: list, city: str):
    for pin, cit in zip(pincodes, city):
        bb_pinc(pin, cit)
        itemno = 0
        #print("----------------------------{}------------------------------".format(cit))
        for EAN, link in zip(products['EAN'], links):
            if EAN != 'None': 
                driver.execute_script("window.open('{}', '_blank')".format(link))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                EAN = EAN
                Title = soup.find('h1', class_='GrE04')
                t = Title.text.strip() if Title else 'None'
                MRP = soup.find('td',class_='_2ifWF')
                m = MRP.text.strip().split('Rs')[1] if MRP else 'None'
                Price = soup.find("td",class_='IyLvo')
                p = Price.text.strip().split('Rs')[1] if Price else 'None'
                #pc = soup.find('span', {'class':'ng-binding'})
                pinco = pin #pc.text.strip() if pc else 'None'

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                EAN = 'None'
                t = products['Name'][itemno]
                m = p = 'None'
            itemno += 1
            if EAN != 'None': info.append((EAN, t, m, p, pinco)) 
            print("%s -- "%count+"EAN: {}, Name: {}, MRP: {}, Price: {}, Pincode: {}".format(EAN, t, m, p, pinco))
            count += 1
    return info
    
#Main function to execute all the functions.
if __name__ == "__main__":
    start = datetime.datetime.now()
    products = pd.read_csv("Generated_Files/items.csv")
    pincodes_df = pd.read_excel('Generated_Files/pincodes/pincodes_bb.xlsx')
    l = bb_links(products)
    driver.get(url)
    with open('Generated_Files/Scrapped_Files/bb_scraper.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now()])
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        items = bb_items_scraper(l, products, count, pincodes_df['Pin Code'], pincodes_df['City'])
        for i in items:
            csvwriter.writerow({'EAN':i[0], 'Name':i[1], 'MRP':i[2], 'Price':i[3], 'Pincode/City': i[4]})
    end = datetime.datetime.now()
    print(end - start)
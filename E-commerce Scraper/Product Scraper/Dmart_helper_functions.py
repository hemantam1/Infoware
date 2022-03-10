from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException
import time
import re
import warnings
import pandas as pd

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

pincode_df = pd.read_excel('Required files/pincodes_dmart.xlsx')
url = 'https://www.dmart.in/'

def dmt_pincode(driver, p):
    """Function to navigate the pincode input operation.

    Args:
        p (int): pincode of the city.
    """
    try:
        driver.find_element(By.CLASS_NAME,"src-client-components-header-__header-module___pincode").click()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'//*[@id="pincodeInput"]').clear()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'//*[@id="pincodeInput"]').send_keys(p)
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/ul/li/button').click()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button').click()
        driver.implicitly_wait(2)
    except:
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'//*[@id="pincodeInput"]').clear()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'//*[@id="pincodeInput"]').send_keys(p)
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/ul/li/button').click()
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button').click()
        driver.implicitly_wait(2)
    time.sleep(1)

def dmt_links_generator(products: list):
    """Generates links based on the product name stored in the excel sheet.

    Args:
        products (list): Product names

    Returns:
        List: Dmart links to product pages.
    """
    links = []
    for i in products:
        if i != 'None':
            links.append('https://www.dmart.in/product/{}/'.format(i))
    return links

def dmt_product_details_scraper(link, csv_writer):
    #Create a temporary dictionary to store the scrapped items.
    information = {}

    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(url)
    time.sleep(1)
    
    for pin in pincode_df['Pin Code']:
        try:
            dmt_pincode(driver, pin)

            driver.execute_script("window.open('{}', '_blank')".format(link))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            #Converting into BeautifulSoup and extracting all the details.
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            Title = soup.find('div', class_='src-client-app-product-details-styles-__text-label-component-module___title-container')
            t = Title.text.strip() if Title else 'None'
            MRP = soup.find('span',class_='src-client-app-product-details-styles-__price-details-component-module___mrp')
            m = MRP.text.strip().split(u'\u20B9')[1] if MRP else 'None'
            Price = soup.find("span",class_='src-client-app-product-details-styles-__price-details-component-module___sp')
            p = Price.text.strip().split(u'\u20B9')[1] if Price else 'None'

            print(f"Name: {t}, MRP: {m}, Price: {p}, Pincode: {pin}")

            information['Name'] = t
            information['MRP'] = m
            information['Price'] = p
            information['Pincode'] = pin

            #CSV writer function to write all the scrapped data to the file.
            csv_writer.writerow({'Pincode': information['Pincode'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price']})

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            print('Element not loading.')
            print(f'------------------------{driver.current_url}-----------------------------')

    driver.close()
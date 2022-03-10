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

pincode_df = pd.read_excel('Required files/pincodes.xlsx')

def amz_pincode(driver, p):
    """Function to navigate the pincode input operation.

    Args:
        p (int): pincode of the city.
    """
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, "//./div[@id='nav-global-location-slot']").click()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "//./input[@class='GLUX_Full_Width a-declarative']").clear()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "//./input[@class='GLUX_Full_Width a-declarative']").send_keys(p)
        driver.implicitly_wait(5)
    except InvalidSessionIdException or NoSuchElementException:
        print('----------Driver error, refreshing the page.---------- {}'.format(driver.current_url))
        driver.close()

    #WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GLUXZipUpdate"]/span')))
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span').click()
    driver.implicitly_wait(5)
    time.sleep(3)

def amz_links_generator(products: list):
    """Generates links based on the ASIN code stored in the excel sheet.

    Args:
        products (list): Product ASIN

    Returns:
        List: Amazon links to product pages.
    """
    links = []
    for i in products:
        if i != 'none':
            links.append('https:/www.amazon.in/dp/{}/'.format(i))
    return links

def amz_product_details_scraper(link, csv_writer):
    #Create a temporary dictionary to store the scrapped items.
    information = {}

    #Setting up the headless mode for the chrome driver to reduce RAM usage.
    #options.add_argument('--headless')
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(link)
    time.sleep(1)
    
    for pin in pincode_df['Pin Code']:
        try:
            amz_pincode(driver, pin)

            #Converting into BeautifulSoup and extracting all the details.
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            ASIN = re.findall(r"(?<=dp/)[A-Z0-9]{10}", link)
            a = ASIN[0] if ASIN else 'None'
            Title = soup.find('span', {'id' : 'productTitle'})
            t = Title.text.strip() if Title else 'None' 
            MRP = soup.find('span', {'class': 'a-price a-text-price a-size-base'}) or soup.find('span', {'class': 'a-price a-text-price'})
            m = MRP.text.split('\u20b9')[1].strip() if MRP else 'None'
            Price = soup.find('span', {'class': 'a-price-whole'})
            p = Price.text.strip() if Price else 'None'
            Pincode = soup.find('span', {'class':'nav-line-2 nav-progressive-content'})
            pin = Pincode.text.strip() if Pincode else 'None'

            print(f"ASIN: {a}, Name: {t}, MRP: {m}, Price: {p}, Pincode: {pin}")

            information['ASIN'] = a
            information['Name'] = t
            information['MRP'] = m
            information['Price'] = p
            information['Pincode'] = pin

            #CSV writer function to write all the scrapped data to the file.
            csv_writer.writerow({'ASIN': information['ASIN'], 'Pincode': information['Pincode'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price']})
        except:
            print('Element not loading.')
            print(f'------------------------{driver.current_url}-----------------------------')
    driver.close()
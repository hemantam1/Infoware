from lib2to3.pgen2 import driver
from lib2to3.pgen2.grammar import opmap_raw
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
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

details = []

def jm_links_generator(website):
    """Function to collect all the links of product present on the offers page.

    Args:
        website (string): Input website as a string which contains the categories and the products to be scraped.

    Returns:
        List: Returns a list of product page URLs which can be then opened and scrapped separately.
    """
    links_to_be_extracted = []
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)

    #Search the page for all the available product categories or pages.
    temp = driver.find_elements(By.XPATH, "//./a[@class='category_name']")
    for t in temp:
        links_to_be_extracted.append(t.get_attribute('href'))

    return links_to_be_extracted

def jm_details_scraper(link, csv_writer):
    """Function to open the product page and scrap the required details and store them in a CSV file.

    Args:
        link (string): Individual product URLs.
        csv_writer (variable): Dictionary writer function.
    """
    information = {}

    options.add_argument("--headless")
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(link)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    jio = re.findall(r"(?<=/)[0-9]{9}", link)
    Title = soup.find('div', class_='title-section')
    t = Title.text.strip() if Title else 'None'
    MRP = soup.find('span',class_='price')
    m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
    Price = soup.find('span',class_='final-price')
    p = Price.text.strip().split('\u20b9')[1] if Price else 'None'

    print(f"JIO: {jio}, Name: {t}, MRP: {m}, Price: {p}, Link: {link}")

    information['JIO'] = jio
    information['Name'] = t
    information['MRP'] = m
    information['Price'] = p
    information['Link'] = link

    csv_writer.writerow({'JIO': information['JIO'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price'], 'Link': information['Link']})

    driver.close()
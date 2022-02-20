from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
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

#driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
details = []

#Function to open the respective pincode page.
def amz_pincode(p, driver):
    """Function to navigate the pincode input operation.

    Args:
        p (int): pincode of the city.
    """
    time.sleep(2)
    try:
        driver.find_element_by_xpath('//*[@id="nav-global-location-popover-link"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').clear()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(p)
        driver.implicitly_wait(5)
    except ElementClickInterceptedException:
        driver.refresh()
        driver.find_element_by_xpath('//*[@id="nav-global-location-popover-link"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').click()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').clear()
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys(p)
        driver.implicitly_wait(5)

    driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
    driver.implicitly_wait(5)
    time.sleep(5)

#Function to generate the links for the products to make it easier to run.
def amz_links_generator(products: list):
    """Generates links based on the ASIN code stored in the excel sheet.

    Args:
        products (list): Product ASIN

    Returns:
        List: Amazon links to product pages.
    """
    links = []
    for i in products:
        links.append('https:/www.amazon.in/dp/{}/'.format(i))
    return links

def amz_links_collector(website):
    """Function to collect all the links of product present on the offers page.

    Args:
        website (string): Input website as a string which contains the categories and the products to be scraped.

    Returns:
        List: Returns a list of product page URLs which can be then opened and scrapped separately.
    """
    links_to_be_extracted = []
    product_page_regex = r'/dp/'
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)
    
    #Search the page for all the available product categories or pages.
    temp = driver.find_elements(By.XPATH, "//./a[@class='a-link-normal  a-color-base a-text-normal']")
    for t in temp:
        #Getting the links from the webelements on the page.
        li = t.get_attribute('href')
        #Separate and store the links based on products and if categories then open and extract product links separately.
        if re.findall(product_page_regex, li):
            links_to_be_extracted.append(li)
        else:
            driver.execute_script("window.open('{}', '_blank')".format(li))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            cat_sub_list = driver.find_elements(By.XPATH, "//./a[@class='a-size-base a-color-base a-link-normal a-text-normal']")
            for sub in cat_sub_list:
                links_to_be_extracted.append(f"{sub.get_attribute('href')}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    return links_to_be_extracted

def amz_details_scraper(link, csv_writer):
    """Function to open the product page and scrap the required details and store them in a CSV file.

    Args:
        link (string): Individual product URLs.
        csv_writer (variable): Dictionary writer function.
    """
    #Create a temporary dictionary to store the scrapped items.
    information = {}

    #Setting up the headless mode for the chrome driver to reduce RAM usage.
    options.add_argument('--headless')
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(link)
    time.sleep(3)

    #Converting into BeautifulSoup and extracting all the details.
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ASIN = re.findall(r"(?<=dp/)[A-Z0-9]{10}", link)
    a = ASIN[0] if ASIN else 'None'
    Title = soup.find('span', {'id' : 'productTitle'})
    t = Title.text.strip() if Title else 'None' 
    MRP = soup.find('span', {'class': 'a-price a-text-price a-size-base'}) or soup.find('span', {'class': 'a-price a-text-price'})
    m = MRP.text.strip().split('\u20b9')[1] if MRP else 'None'
    Price = soup.find('span', {'class': 'a-price-whole'})
    p = Price.text.strip() if Price else 'None'
    Pincode = soup.find('span', {'class':'nav-line-2 nav-progressive-content'})
    pin = Pincode.text.strip() if Pincode else 'None'

    print(f"ASIN: {a}, Name: {t}, MRP: {m}, Price: {p}, Pincode: {pin}, Link: {link}")

    information['ASIN'] = a
    information['Name'] = t
    information['MRP'] = m
    information['Price'] = p
    information['Pincode'] = pin
    information['Link'] = link

    #CSV writer function to write all the scrapped data to the file.
    csv_writer.writerow({'ASIN': information['ASIN'], 'Pincode': information['Pincode'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price'], 'Link': information['Link']})

    driver.close()

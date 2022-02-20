from bs4 import BeautifulSoup
from numpy import product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
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

def bb_scroll(driver):
    """Since BigBasket has a scroll down style website, this function will scroll till all the products have loaded into view.

    Args:
        driver (selenium.webdriver): driver function to control the webpage.
    """
    a = ActionChains(driver)
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/footer/div[1]/div[3]")
    while driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/product-deck/section/div[2]/div[4]/div[3]/button'):
        a.move_to_element(element).perform()
        try:
            show_more_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/product-deck/section/div[2]/div[4]/div[3]/button")
            show_more_element.click()
            time.sleep(3)
        except:
            time.sleep(3)
        
        #Check for the end of the page.
        if driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/product-deck/section/div[2]/div[4]/div[4]').text == "--That's all folks--":
            break

def bb_combos_links_generator(website):
    """Function to collect all the links of product present on the offers page.

    Args:
        website (string): Input website as a string which contains the products to be scraped.

    Returns:
        List: Returns a list of product page URLs which can be then opened and scrapped separately.
    """
    #Create an empty list to store the links.
    bb_links = []

    #Loading the driver and the website.
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)

    #Calling the Scroll function to load the entire page.
    bb_scroll(driver)

    #Collect all the product links and store it into bb_links.
    products = driver.find_elements(By.XPATH, "//./div[@qa='product_name']/a")
    for prod in products:
        bb_links.append(prod.get_attribute('href'))

    driver.close()
    return bb_links

def bb_details_scraper(website, csv_writer):
    """BigBasket details scraper function which scrapes EAN, Name, MRP, and Price.

    Args:
        website (string): URL of the product page.
        csv_writer (csv writer function)): Writes the scrapped data to a CSV file.
    """
    #Create an empty dictionary to store the data.
    information = {}

    #Loading the driver and the website. Including Headless mode to reduce RAM usage.
    options.add_argument('--headless')
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)

    #Passing the webpage into BeautifulSoup and extracting all the details.
    sp = BeautifulSoup(driver.page_source, 'html.parser')
    eancode = sp.find('tbody')
    ec = eancode['id'] if eancode['id'] else "None"
    name = sp.find('h1', class_='GrE04')
    n = name.text.strip() if name else "None"
    mrp = sp.find('td',class_='_2ifWF')
    m = mrp.text.strip() if mrp else "None"
    price = sp.find("td",class_='IyLvo')
    p = price.text.strip() if price else "None"

    print("EAN Code: {}, Name: {}, MRP: {}, Price: {}".format(ec, n, m, p))

    information['EAN'] = ec
    information['Name'] = n
    information['MRP'] = m
    information['Price'] = p

    #CSV writer function to write all the scrapped data to the file.
    csv_writer.writerow({'EAN': information['EAN'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price']})

    driver.close()
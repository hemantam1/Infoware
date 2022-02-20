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

def scroll(driver):
    #Since BigBasket has a scroll down style website, this function will scroll till all the products have loaded into view.
    a = ActionChains(driver)
    element = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/footer/div[1]/div[3]")
    count = 0
    while driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/product-deck/section/div[2]/div[4]/div[3]/button'):
        count += 1
        a.move_to_element(element).perform()
        try:
            show_more_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/product-deck/section/div[2]/div[4]/div[3]/button")
            show_more_element.click()
            time.sleep(3)
        except:
            time.sleep(3)
        
        #Limit the number of pages loaded to keep the scraping in control.
        if count >= 10:
            break

def bb_offers_links_generator(website):
    """Function to collect all the links of product present on the offers page.

    Args:
        website (string): Input website as a string which contains the products to be scraped.

    Returns:
        List: Returns a list of product page URLs which can be then opened and scrapped separately.
    """
    bb_links = []

    #Loading the driver and the website.
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)

    #Calling the Scroll function to load the entire page.
    scroll(driver)

    #Collect all the product links and store it into bb_links.
    products = driver.find_elements(By.XPATH, "//./div[@qa='product_name']/a")
    for prod in products:
        bb_links.append(prod.get_attribute('href'))

    driver.close()
    return bb_links

def bb_details_scraper(website, csv_writer):
    information = {}

    #Loading the driver and the website.
    options.add_argument('--headless')
    driver = webdriver.Chrome('C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
    driver.get(website)

    #Wait for the website to load.
    driver.implicitly_wait(2)
    time.sleep(4)

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

    csv_writer.writerow({'EAN': information['EAN'], 'Name': information['Name'], 'MRP': information['MRP'], 'Price': information['Price']})

    driver.close()
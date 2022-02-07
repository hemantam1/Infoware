from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

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

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options) #C:\Users\ARYAN\Downloads\chromedriver_win32
url = 'https://www.bigbasket.com/pb/all-brands/'
headers = ['Company', 'Number of Products', 'Link']

def bb_links(link_list: list) -> list:
    links = []
    for l in link_list:
        links.append('https://www.bigbasket.com/{}'.format(l['href']))
    return links

def bb_companies(source: str) -> list:
    driver.get(source)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    companies = []
    for c in soup.find_all('ul', {'class':'uiv2-listing-brands-views'}):
        for cmps in c.find_all(href=True):
            companies.append('https://www.bigbasket.com/{}'.format(cmps['href']))
    return companies

def bb_info_scraper(res: list) -> list:
    inf = []
    for company in res:
        driver.execute_script("window.open('{}', '_blank')".format(company))
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(1)
        pg = driver.page_source
        sp = BeautifulSoup(pg, 'html.parser')
        name = sp.find('h2', {'class':'tabsEx'})
        n = name.text.strip().split('(')[0] if name else 'None'
        no = sp.find('span', {'id':'uiv2-num-products'})
        num = no.text.strip() if no else 'None'
        #print("%s -- "%count + "{}, {}".format(n, num))
        inf.append((n, num, company))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return inf

if __name__ == '__main__':
    driver.get(url)
    time.sleep(5)
    info = []
    count = 0
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    letters = soup.find('ul', {'class':'uiv2-sorting-list-alpha'})
    let = letters.find_all(href=True)
    link = bb_links(let)
    with open('Product_scraper/Generated_Files/bb_prod_count.csv', 'w+', newline='') as f:
        csvwriter = csv.DictWriter(f, fieldnames=headers)
        csvwriter.writeheader()
        for l in link:
            res = bb_companies(l)
            info = bb_info_scraper(res)
            csvwriter.writerow({'Company':info[0], 'Number of Products': info[1], 'Link':info[2]})
        driver.close()
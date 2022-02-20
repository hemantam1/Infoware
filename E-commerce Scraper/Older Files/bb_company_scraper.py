from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from googlesearch import search
import csv
import datetime

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
info = []

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver', options=options)
url = 'https://www.bigbasket.com/'
count = 0
headers = ['Name', 'BB_Link', 'Result']
with open('./Generated_Files/bb_company_scraper.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()
    for i in range(0, 7):
        driver.execute_script("window.open('https://www.bigbasket.com/pb/all-brands/{}/?nc=abp', '_blank')".format(i))
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(1)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        alphabet = soup.find_all('div', {'class':'uiv2-listing-brands-cover'})
        for a in alphabet:
            name = a.find_all(href=True)
            link = a.find_all(href=True)
            for n,l in zip(name, link):
                query = n.text.strip()
                for j in search(query, tld='com', lang='en', num=1, start=0, stop=1, pause=0.9):
                    count += 1
                    csvwriter.writerow({'Name':n.text.strip(), 'BB_Link':"https://www.bigbasket.com/{}".format(l['href']), 'Result':j})
                    #info.append((n.text.strip(), "https://www.bigbasket.com/{}".format(l['href']), j))
                    #print("{} -- ".format(count)+n.text.strip(), "https://www.bigbasket.com/{}".format(l['href']), j)
        time.sleep(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
driver.close()


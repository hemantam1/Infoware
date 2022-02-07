from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv
import datetime

start = datetime.datetime.now()

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

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
url = 'https://www.bigbasket.com/offers/?nc=nb#!page=1'
a = ActionChains(driver)
driver.get(url)
headers = ['EAN', 'Name', 'Pincode', 'MRP', 'Price']
pincodes = {'Delhi':'110001', 'Mumbai':'400001', 'Bangalore':'560300', 'Hyderabad':'500002', 'Kolkata':'700012'}
count = 0

for i in range(0, 20):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

pincode = driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/a/span/span[1]')
city = driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/a/span/span[2]')

soup = BeautifulSoup(driver.page_source, 'html.parser')
aad = soup.find_all('div', qa ='product')
with open('./Generated_Files/Scrapped_Files/bb-offers.csv', 'w', newline='') as f:
    tme = datetime.datetime.now()
    writer = csv.writer(f)
    writer.writerow([datetime.date.today(), tme.strftime("%H:%M:%S") , url])
    csvwriter = csv.DictWriter(f, fieldnames=headers, dialect='excel')
    csvwriter.writeheader()
    for aa in aad:
        count += 1
        link = aa.find('a')
        driver.execute_script("window.open('https://www.bigbasket.com%s', '_blank')"%(link['href']))
        driver.switch_to.window(driver.window_handles[1])
        sp = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)

        eancode = sp.find('tbody')
        ec = eancode['id'] if eancode['id'] else "None"
        name = sp.find('h1', class_='GrE04')
        n = name.text.strip() if name else "None"
        pincod = sp.find('div', class_='_1N37e')
        pincode = pincod.text.strip() if pincod else "None"
        """for key, value in pincodes.items():
            driver.implicitly_wait(1)
            try:
                driver.find_element_by_class_name('_1N37e').click() #location
                driver.implicitly_wait(1)
            except ElementClickInterceptedException:
                driver.refresh()
                driver.implicitly_wait(1)
                driver.find_element_by_class_name('_1N37e').click()
                driver.implicitly_wait(1)

            driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[1]/span').click() #dropdown list
            driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[1]/input').send_keys(key, Keys.ENTER)#city
            driver.implicitly_wait(1)
            if value != '':
                driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[2]/input').send_keys(value)
                try:
                    driver.find_element_by_class_name('oXkKp').click()
                except:
                    pass
            driver.implicitly_wait(1)
            driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/form/button').click()
            driver.implicitly_wait(1)"""
        m = sp.find('td',class_='_2ifWF')
        mrp = m.text.strip() if m else 'None'
        p = sp.find("td",class_='IyLvo')
        price = p.text.strip() if p else 'None'

        print("%s -- "%count+"EAN Code: {}, Pincode: {}, Name: {}, MRP: {}, Price: {}".format(ec, pincode, n, mrp, price))
        csvwriter.writerow({'EAN': ec, 'Pincode': pincode, 'Name': n, 'MRP': mrp, 'Price': price})
    
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
end = datetime.datetime.now()
print(end - start)
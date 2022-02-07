from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

#Some arguments that help for smooth and faster execution of the script.
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

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver', options=options)
url = 'https://www.bigbasket.com/product/all-categories/'
driver.get(url)
driver.maximize_window()
headers = ['EAN', 'Name', 'MRP', 'Price']
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

#Implementing function was causing issues so a simple nested loop structure to generate the product details.
categories = soup.find('div', class_='uiv2-myaccount-wrapper uiv2-mar-t-35 uiv2-search uiv2-all-categories-wrapper')
with open('./Generated_Files/bb_scraper_cat.csv', 'w', newline='') as f:
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()
	#Grabs category and subcategory from the website.
    for cat, sub in zip(categories.find_all('div', class_='dp_headding'), categories.find_all('ul', class_='uiv2-search-category')):
        print('Category:'+cat.text.strip())
        a = []
	#Generates the link to which we have to navigate to.
        for s in sub.find_all('li'):
            link = s.find('a', href=True)
            #print('\tSub-Category:'+s.text.strip())
            driver.execute_script("window.open('https://www.bigbasket.com/{}', '_blank')".format(link['href']))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
            sup = BeautifulSoup(driver.page_source, 'html.parser')
            products = sup.find_all('div', qa='product')
            for p in products[:10]:
                link = p.find('a')
                driver.execute_script("window.open('https://www.bigbasket.com%s', '_blank')"%(link['href']))
                driver.switch_to.window(driver.window_handles[2])
                sp = BeautifulSoup(driver.page_source, 'html.parser')
                time.sleep(5)

                eancode = sp.find('tbody')
                ec = eancode['id'] if eancode['id'] else "None"
                name = sp.find('h1', class_='GrE04')
                n = name.text.strip() if name else "None"
                mrp = sp.find('td',class_='_2ifWF')
                m = mrp.text.strip() if mrp else "None"
                price = sp.find("td",class_='IyLvo')
                p = price.text.strip() if price else "None"
                
                #print("\t\t"+"EAN Code: {}, Name: {}, MRP: {}, Price: {}".format(ec, n, m, p))
                csvwriter.writerow({'EAN': ec, 'Name': n, 'MRP': m, 'Price': p})
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

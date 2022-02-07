from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
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

start = datetime.datetime.now()

driver = webdriver.Chrome(executable_path='C:\\Users\\ARYAN\\Downloads\\chromedriver_win32\\chromedriver', options=options)
url = 'https://www.bigbasket.com/sp/2106070_combos/?nc=b-cp-hp-sec3&b_t=cp_hp_sec3&b_camp=hp_cmc_m_5_june_topstrip_60_250521&t_from_ban=3132648&t_pos=5&t_ch=desktop#!page=3'
a = ActionChains(driver)
driver.get(url)
headers = ['EAN', 'Name', 'MRP', 'Price', 'Type']
pincode = driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/a/span/span[1]')
city = driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/a/span/span[2]')

com = pro = 0 
while driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[3]'):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    try:
        load = driver.find_element_by_xpath('//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[3]')
        load.click()
    except:
        break
    time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
aad = soup.find_all('div', qa ='product')
with open('./Generated_Files/combos.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now(), pincode.text.strip(), city.text.strip(), url])
    
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()
    for a in aad:
        link = a.find('a')
        driver.execute_script("window.open('https://www.bigbasket.com%s', '_blank')"%(link['href']))
        driver.switch_to.window(driver.window_handles[1])
        sp = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(5)
        
        com += 1
        eancode = sp.find('tbody')
        ec = eancode['id'] if eancode['id'] else "None"
        name = sp.find('h1', class_='GrE04')
        n = name.text.strip() if name else "None"
        mrp = sp.find('td',class_='_2ifWF')
        m = mrp.text.strip() if mrp else "None"
        price = sp.find("td",class_='IyLvo')
        p = price.text.strip() if price else "None"
    
        print("%s--"%com+"EAN Code: {}, Name: {}, MRP: {}, Price: {}, Type: Combo".format(ec, n, m, p))
        csvwriter.writerow({'EAN': ec, 'Name': n, 'MRP': m, 'Price': p, 'Type': 'Combo'})
        
        l = sp.find_all('a', class_='_3ROsT _3bj9B rippleEffect')
        if l != '':
            for i in l:
                driver.execute_script("window.open('https://www.bigbasket.com%s', '_blank')"%(i['href']))
                driver.switch_to.window(driver.window_handles[2])
                s = BeautifulSoup(driver.page_source, 'html.parser')
                time.sleep(5)

                pro += 1    
                eancode = s.find('tbody')
                ec = eancode['id'] if eancode['id'] else "None"
                name = s.find('h1', class_='GrE04')
                n = name.text.strip() if name else "None"
                mrp = s.find('td',class_='_2ifWF')
                m = mrp.text.strip() if mrp else "None"
                price = s.find("td",class_='IyLvo')
                p = price.text.strip() if price else "None"
            
                print("\t%s-"%pro+"EAN Code: {}, Name: {}, MRP: {}, Price: {}, Type: Product".format(ec, n, m, p))
                csvwriter.writerow({'EAN': ec, 'Name': n, 'MRP': m, 'Price': p, 'Type': 'Product'})

                driver.close()
                driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
end = datetime.datetime.now()
print(end - start)
#driver.close()

import concurrent.futures
from jiomart_offers_functions import *
import csv
import datetime
from itertools import repeat

url = 'https://www.jiomart.com/all-topdeals'

headers = ['JIO', 'Name', 'MRP', 'Price', 'Link']

#Calling and storing all the links in a list to be futhur processed.
links = jm_links_generator(url)

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/jiomart-offers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(jm_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
import concurrent.futures
from bb_offers_functions import *
import csv
import datetime
from itertools import repeat

url = "https://www.bigbasket.com/offers/?nc=nb#!"
headers = ['EAN', 'Name', 'MRP', 'Price']

#Calling and storing all the links in a list to be futhur processed.
links = bb_offers_links_generator(url)

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/bb-offers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(bb_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
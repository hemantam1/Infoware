import concurrent.futures
from amazon_offers_functions import *
import csv
import datetime
from itertools import repeat
import time

#Assign the URL for the Amazon offers website.
url = 'https://www.amazon.in/deals?ref_=nav_cs_gb'
headers = ['ASIN', 'Name', 'MRP', 'Price', 'Pincode', 'Link']

#Calling and storing all the links in a list to be futhur processed.
links = amz_links_collector(url)

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/amazon-offers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    #Assigning worker threads to improve the scraping speed.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(amz_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
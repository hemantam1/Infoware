import concurrent.futures
import pandas as pd
from Dmart_helper_functions import *
import csv
import datetime
from itertools import repeat

print("-----Dmart-----")

#Assign the products for the Dmart's website.
headers = ['Name', 'MRP', 'Price', 'Pincode']
product_df = pd.read_csv("Required files/items.csv")

#Calling and storing all the links in a list to be futhur processed.
links = dmt_links_generator(product_df['dmart'])

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/dmart-products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    #Assigning worker threads to improve the scraping speed.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(dmt_product_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
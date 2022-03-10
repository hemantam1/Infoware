import concurrent.futures
import pandas as pd
from Amazon_helper_functions import *
import csv
import datetime
from itertools import repeat

#Assign the URL for the Amazon offers website.
url = 'https://www.amazon.in/'
headers = ['ASIN', 'Name', 'MRP', 'Price', 'Pincode']
product_df = pd.read_csv("Required files/items.csv")

#Calling and storing all the links in a list to be futhur processed.
links = amz_links_generator(product_df['ASIN'])

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/amazon-products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    #Assigning worker threads to improve the scraping speed.
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(amz_product_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
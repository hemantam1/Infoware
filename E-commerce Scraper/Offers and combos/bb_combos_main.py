import concurrent.futures
from bb_combos_functions import *
import csv
import datetime
from itertools import repeat

url = 'https://www.bigbasket.com/sp/2202067-combos/?nc=b-cp-hp-sec3&b_t=cp_hp_sec3&b_camp=hp_topstrip_m_combostore_190x60_250122png&t_from_ban=4084651&t_pos=5&t_ch=desktop'
headers = ['EAN', 'Name', 'MRP', 'Price']

#Calling and storing all the links in a list to be futhur processed.
links = bb_combos_links_generator(url)
#print(links)

start = datetime.datetime.now()
#Opening the CSV file to store all the scrapped data.
with open('Scrapped_Files/bb-combos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.datetime.now()])
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        titles = list(executor.map(bb_details_scraper, links, repeat(csvwriter)))

end = datetime.datetime.now()
print(end - start)
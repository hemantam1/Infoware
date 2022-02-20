from bb_combos_functions import bb_details_scraper
import csv

url = "https://www.amazon.in/LG-inch-60-96-Gaming-Monitor/dp/B06XDY3SJF/?_encoding=UTF8&pd_rd_w=TEe4I&pf_rd_p=6aeb164c-387d-440e-8808-65edf45c4683&pf_rd_r=KRZK2TA33PSD5WPDYJSE&pd_rd_r=41838823-5974-4d9f-b57d-d07c391f84dc&pd_rd_wg=SjRrn&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
headers = ['EAN', 'Name', 'MRP', 'Price']

with open('Scrapped_Files/bb-offers-test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    csvwriter = csv.DictWriter(f, fieldnames=headers)
    csvwriter.writeheader()
    bb_details_scraper(url, csvwriter)


#Vadodarhttps://www.amazon.in/Melomane-Melophones-Headphone-Power-Packed-Ergonomic/dp/B08PZ7KF2H/?_encoding=UTF8&pd_rd_w=K9rSp&pf_rd_p=d49d3a1b-c6b5-498e-a27d-7d911352ee4d&pf_rd_r=TXXC847KNQ7G1N4XM69F&pd_rd_r=9a99398e-5429-47fa-bf3b-fc39fd1e1110&pd_rd_wg=f3rzd&ref_=pd_gw_unk
#Delhi: https://www.amazon.in/Melomane-Melophones-Headphone-Power-Packed-Ergonomic/dp/B08PZ7KF2H/?_encoding=UTF8&pd_rd_w=K9rSp&pf_rd_p=d49d3a1b-c6b5-498e-a27d-7d911352ee4d&pf_rd_r=TXXC847KNQ7G1N4XM69F&pd_rd_r=9a99398e-5429-47fa-bf3b-fc39fd1e1110&pd_rd_wg=f3rzd&ref_=pd_gw_unk
import xml.etree.ElementTree as xet
import pandas as pd
import os
import datetime
import xml

def attributeChecker(root, word, subword):
    try:
        temp = root.find('{}'.format(word))
        wo = temp.find('{}'.format(subword))
        w = wo.text.strip()
    except:
        w = ''
    return w

start = datetime.datetime.now()
cols = ['Handle', 'Metafield:external_link.redirecting[string]', 'Handle-Old', 'Title-Old', 'Title',
            'Size', 'Color', 'Body (HTML)', 'Vendor', 'Type', 'Tags Command', 'Tag', 'Published',
            'Variant Command', 'option1 Name', 'option1 Value', 'option2 Name', 'option2 Value',
            'option3 Name', 'option3 Value', 'option4 Name', 'option4 Value', 'option5 Name',
            'option5 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',
            'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service',
            'Variant Price', 'Variant Compare at Price', 'Variant Requires Shipping',
            'Variant Taxable', 'Variant Barcode', 'Image Command', 'Image Src', 'Image Position',
            'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description',
            'Google Shopping metafields', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code',
            'Cost per item', 'Status', 'Metafield:currency', 'Metafield:country', 'Metafield:storename']
count = 0
for filename in os.listdir('.\Extracted_files'):
    count += 1
    print(f"{count}: Processing {filename}...")
    xmlparse = xet.parse(f'Extracted_files/{filename}')
    root = xmlparse.getroot()
    rows = []
    header = root.find('header')
    merchname = header.find('merchantName')
    mn = merchname.text.strip()
    for i in root.findall('product'):
        try:
            #Handle, Handle-Old, Title-Old, Title
            handle = i.attrib.get('name', '')
            handlet = handle if handle else ''
            #Metafield:external_link.redirecting[string]
            melrt = attributeChecker(i, 'URL', 'product')
            """melr = i.find('URL')
            melrt = attributeChecker(melr.find('product'))"""
            #Size
            sizet = attributeChecker(i, 'attributeClass', 'Size')
            #Color
            colort = attributeChecker(i, 'attributeClass', 'Color')
            #Body (HTML)
            bodyt = attributeChecker(i, 'description', 'long')
            #Vendor
            vendort = attributeChecker(i, 'brand', 'brand')
            #Option 4 Value
            option4vt = attributeChecker(i, 'attributeClass', 'Gender')
            #Option 5 Value
            option5vt = attributeChecker(i, 'attributeClass', 'Age')
            #SKU Number
            sku = i.attrib.get('sku_number', '')
            skut = sku if sku else ''
            #Variant Price
            variantpt = attributeChecker(i, 'price', 'retail')
            #Image Src
            isrct = attributeChecker(i, 'URL', 'productImage')
            #Metafield:currency
            curr = i.find('price')
            currt = curr.attrib.get('currency', '') if curr.attrib.get('currency', '') else ''
            tc = 'Merge'
            op1 = 'Size'
            op2 = 'Material'
            op3 = 'Color'
            op4 = 'Gender'
            op5 = 'Age'
            vip = 'deny'
            vfs = 'manual'

            rows.append({'Handle': handlet,
            'Metafield:external_link.redirecting[string]': melrt,
            'Handle-Old': handlet,
            'Title-Old': handlet,
            'Title': handlet,
            'Size': sizet,
            'Color': colort,
            'Body (HTML)': bodyt,
            'Vendor': vendort,
            'Type': '',
            'Tags Command': tc,
            'Tag': '',
            'Published': '',
            'Variant Command': tc,
            'option1 Name': op1,
            'option1 Value': sizet,
            'option2 Name': op2,
            'option2 Value': '',
            'option3 Name': op3,
            'option3 Value': colort,
            'option4 Name': op4,
            'option4 Value': option4vt,
            'option5 Name': op5,
            'option5 Value': option5vt,
            'Variant SKU': skut,
            'Variant Grams': 0,
            'Variant Inventory Tracker': '',
            'Variant Inventory Qty': '',
            'Variant Inventory Policy': vip,
            'Variant Fulfillment Service': vfs,
            'Variant Price': variantpt,
            'Variant Compare at Price': variantpt,
            'Variant Requires Shipping': '',
            'Variant Taxable': '',
            'Variant Barcode': '',
            'Image Command': tc,
            'Image Src': isrct,
            'Image Position': '',
            'Image Alt Text': '',
            'Gift Card': '',
            'SEO Title': handlet,
            'SEO Description': bodyt,
            'Google Shopping metafields': '',
            'Variant Image': '',
            'Variant Weight Unit': '',
            'Variant Tax Code': '',
            'Cost per item': variantpt,
            'Status': 'active',
            'Metafield:currency': currt,
            'Metafield:country': '',
            'Metafield:storename': mn})

        except xml.etree.ElementTree.ParseError as error:
            print(f'{filename} process stopped.')
            break
            
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv('csv/{}.csv'.format(filename.split('.xml')[0]))

print('All files have been converted!')
print(datetime.datetime.now() - start)
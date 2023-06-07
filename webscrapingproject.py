from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import csv
import datetime
import pandas as pd

# ctrl + (] or [) to indent
# ctrl + / to comment 

# def check_price():

html_text = requests.get('https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=Nintendo+Switch+Oled&_sacat=0&LH_TitleDesc=0&LH_Auction=1&LH_Sold=1&LH_Complete=1&_sop=13').text
soup = BeautifulSoup(html_text, 'lxml')
# Get all listings after the first instance
products = soup.find_all('div', class_ = 's-item__info clearfix')[1:]
# RegEx for retrieving floating numbers from a string
pattern = r"\d*\.\d+|\d+\.\d*"
today = datetime.date.today()
'''
print('Filter listings by condition')
# Allow user to filter listings by chosen condition 
chosen_codition = input('>')
print(f'Filtering out {chosen_codition}')
'''

# Loop through all items in products list and get specfic information
for product in products:
    condition = product.find('span', class_ = 'SECONDARY_INFO').text 
    title = product.find('span', role = 'heading').text
    price = product.find('span', class_ = 's-item__price').text
    # Use Regex to pull out numbers and convert to float
    price = float(re.search(pattern, price).group())
    sale_date = product.find('span', class_ = 'POSITIVE').text.replace('Sold ', '').strip()
    url = product.a['href']
    postage_cost = product.find('span', class_ = 's-item__shipping s-item__logisticsCost').text.strip()
    # Use Regex to pull out numbers
    postage_cost = re.search(pattern, postage_cost)
    # If postage_cost exists, extract the text by using .group()
    if postage_cost:
        # convert to string to float
        postage_cost = float(postage_cost.group())
    # If not, default to 0.00
    else:
        postage_cost = 0.00

    total_cost = price + postage_cost
    # If  chosen_condition exists in the condition variable, only show these listings 
    #if chosen_codition in condition:

    # Create column headers for csv
    header = ['Title', 'Condition', 'Price', 'Sale_Date', 'Postage', 'Total_Cost', 'Import_Date', 'URL']

    # Specify data to import into columns
    data = [title, condition, price, sale_date, postage_cost, total_cost, today, url]

    # Append data to the csv
    with open('eBayNintendoSwitchOledDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        # Write the header variable to the csv
        # writer.writerow(header)
        writer.writerow(data)


    # print all values
    # print(f'''
    # Title: {title}
    # Condition: {condition}
    # Price: {price}
    # Sale_Date: {sale_date}
    # Postage: {postage_cost}
    # URL: {url}
    # '''
    # )

    
#     while(True):
#         check_price()
#         time.sleep(5)

# Read the csv 
df = pd.read_csv('eBayNintendoSwitchOledDataset.csv')

print(df)

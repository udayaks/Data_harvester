
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import re
import lxml
from datetime import datetime
import os

#____initializing date & time for output file name
today = datetime.now().strftime('%m%d_%H%M')

# """____for input and output path____"""

root_path = os.path.dirname(os.path.abspath(__file__))
# root_path = os.getcwd()
input_path = os.path.join(root_path, "input")
output_path = os.path.join(root_path, "output")

#___initializing Webdriver
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

collectionsetc_data = pd.DataFrame(columns=['url', 'regular_price', 'sale_price', 'schema_price'])

list_url = pd.read_csv(os.path.join(input_path,'url.csv'))['url'].values[-1000:]

def collection_p_scraper(url):
    response = driver.page_source
    soup = BeautifulSoup(response, 'lxml')

    schema_s = soup.find_all('script', {'id': 'jsonLd'})
    if schema_s ==[]:
        schema_price = 'No Schema Price'

    else:
        for i in schema_s:
            schema_price =re.findall('"price":"[0-9]*.[0-9]*"',str(i))

    regular_s = soup.find_all('span',{'class':'regular-price'})
    if regular_s ==[]:
        regular_price = 'No Regular Price'

    else:
        for i in regular_s:
            regular_price = i.text

    sale_s = soup.find_all('span',{'class':'sale-price'})
    if sale_s ==[]:
        sale_price = 'No Sale Price'
    else:
        for i in sale_s:
            sale_price = i.text

    sdata = [[str(url), str(regular_price), str(sale_price), str(schema_price)]]      
    n_data = pd.DataFrame(sdata,columns=['url', 'regular_price', 'sale_price', 'schema_price'])
    
    return n_data




count = 0
for i in list_url:
    driver.get(i)
    data = collection_p_scraper(i)
    collectionsetc_data = collectionsetc_data.append(data, ignore_index=True)
    if count%100 ==0:
        collectionsetc_data.to_csv(os.path.join(output_path, "collection_etc_price_"+today+".csv"), sep="\t", encoding="utf-8")
    print(count)   
    count = count +1








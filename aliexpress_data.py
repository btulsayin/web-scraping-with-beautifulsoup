# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json

#urun ismi,link,resim çekme
productName,href,image,comment = [],[],[],[]

r = requests.get("https://www.aliexpress.com/")
data = r.text
soup = BeautifulSoup(data)
for all_product_content in soup.find_all('div', attrs = { 'class' : 'categories-list-box' }):
    for link in all_product_content.find_all('a'):
        print(link.get('href'))
        subcategories_url=link.get('href')
        r = requests.get("http://www.aliexpress.com/category/100003109/women-clothing-accessories.html")
        data = r.text
        soup = BeautifulSoup(data)
        for all_product_content in soup.find_all('div', attrs = { 'class' : 'pic' }):
            print(all_product_content)

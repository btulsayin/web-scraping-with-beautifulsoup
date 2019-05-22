# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os,time
from decimal import Decimal, ROUND_HALF_UP
from urllib.request import urlopen

main_url= "https://www.boyner.com.tr/"
page_url= "https://www.boyner.com.tr/kadin-c-1"
root_folder_path = os.path.dirname(__file__)

def select_page(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.text, "lxml")
    return r, soup

def createFolder(foldername,second_subcategories_name):
    subfolder_name=foldername
    second_subfolder_name=second_subcategories_name
    foldername=os.path.join(root_folder_path, "moda", subfolder_name,second_subfolder_name)
    if not os.path.exists(foldername):
        print("**Klasor Mevcut Degil**")
        os.makedirs(foldername)
    else:
        print("**Klasor Mevcut**")
    
    return foldername

#verilerin isimlerini,url gibi istenilen detaylarını almak için         
def image_detail(all_product_content,subcategories_name):
#    print("KATEGORİ ADI: {}".format(subcategories_name))
    for link in all_product_content.find_all('a',attrs = { 'class' : 'product-figure ecommerceClick' }):
        print("Image href: {}".format(link.get('href')))
        image_url=link.get('href')
        sub_page_url=main_url+image_url
        print("****sub_page_url**** {}".format(sub_page_url))
        seb_req, subpage_soup = select_page(sub_page_url)
        for link in all_product_content.find_all('img', attrs = { 'class' : 'lazy' }):
            print("***2***")
            print(link)
            print("Image: {}".format(link.get('data-original')))
   
def image_link(soup,subcategories_name):
    for all_product_content in soup.find_all('div', attrs = { 'class' : 'product-figure-wrap' }):
        image_detail(all_product_content, subcategories_name)
 
if __name__ == "__main__":            
    req, soup = select_page(page_url)    
    sub_categori_class = soup.find_all('div',
                                       attrs = {'class' : 'sidebar-box'})
    if req.status_code == 200:
        for all_product_content in sub_categori_class:
            for link in all_product_content.find_all('a'):
                sub_page_url = link.get('href').split("/")[-1]                
                subcategories_name=sub_page_url.split("/")[-1]
                print("subcategories_name: {}".format(subcategories_name)) 
#                if subcategories_name=="kadin-giyim":
#                    print("***kadin***")
                sub_page_url=main_url+sub_page_url
                print("sub_page_url: {}".format(sub_page_url))
                
                #START calculate sub_page number 
                if subcategories_name!="kadin-jean-c-100109":
                    print("evet")
                    req, sub_soup = select_page(sub_page_url)                
                    tt = sub_soup.find("span", {"class": "grey"})    
                    value=tt.text.replace("(", "")
                    value=value.replace(")", "")
                    print(value)
                    val = float(value)/90 # it has 90 product on each page     
                    val = Decimal(str(val))
                    print("**val** {}".format(val))
                    page_number = int(Decimal(val.quantize(Decimal('1'),
                                                       rounding=ROUND_HALF_UP)))
                    if page_number == 0: page_number = 1
#               #END calculate sub_page number 
                    for i in range(1, page_number + 1):
                        pages_subcategories_url="{}/{}/".format(sub_page_url, i)
                        print("pages_subcategories_url: {}".format(pages_subcategories_url))
                        time.sleep(10)
                        seb_req, subpage_soup = select_page(pages_subcategories_url)
                        try:
                            image_link(subpage_soup, subcategories_name)
                        except:
                            print("Hata Olustu")
                    
                else:
                    print("hayir")

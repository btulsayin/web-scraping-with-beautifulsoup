# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os,time
from decimal import Decimal, ROUND_HALF_UP
from urllib.request import urlopen

main_url= "https://www.gittigidiyor.com"
page_url= "https://www.gittigidiyor.com/cadde/kategori/moda"
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
def image_detail(all_product_content,subcategories_name,second_subcategories_name):
    print("KATEGORİ ADI: {} SECOND KATEGORİ: {}".format(subcategories_name,second_subcategories_name))
    for link in all_product_content.find_all('a'):
        print("Image href: {}".format(link.get('href')))
    for link in all_product_content.find_all('img'):
#        print("Image: {}".format(link.get('data-original')))
        image_link=link.get('data-original')
        image_name=os.path.split(image_link)[1]
        print("Image Url: {}".format(image_link))
        print("Image Save Name: {}".format(os.path.split(image_link)[1]))
        print(image_name)
    for link in all_product_content.find_all('img'):
        print("Image Name: {}".format(link.get('alt')))
        
    save_image(image_link,image_name,subcategories_name,second_subcategories_name)  
        
def image_link(soup,subcategories_name,second_subcategories_name):
    for all_product_content in soup.find_all('div', attrs = { 'class' : 'productImageContent' }):
#            print("all_product_content: {}".format(all_product_content))
            image_detail(all_product_content, subcategories_name,second_subcategories_name)

#resimleri istenilen klasöre indirmek için 
def save_image(imgUrl,image_name,subcategories_name,second_subcategories_name):
    try:
        #kaydedilmek istenen klasörün yolu belirtilir.
        foldername = createFolder(subcategories_name,second_subcategories_name)
        filePath = os.path.join(foldername, image_name)
        print("filePath: {}".format(filePath))
        
        try:
            print("***KAYDET***")
            imgData = urlopen(imgUrl).read()
            output = open(filePath,'wb')
            output.write(imgData)
            output.close()
        except:
            print("Kaydedilemedi...")
    except:
        print("***Hata Olustu***")
        
if __name__ == "__main__":            
    req, soup = select_page(page_url)    
    sub_categori_class = soup.find_all('li',
                                       attrs = {'class' : 'filter_sub_title'})
    if req.status_code == 200:
        for all_product_content in sub_categori_class:
        #    print(all_product_content)
            for link in all_product_content.find_all('a'):
                print(link.get('href'))
                sub_page_url = link.get('href')                
                subcategories_name=sub_page_url.split("/")[-1]
                print("subcategories_name: {}".format(subcategories_name)) 
                sub_page_url=main_url+sub_page_url
                print("sub_page_url: {}".format(sub_page_url))
                seb_menu_req, sub_menu_soup=select_page(sub_page_url)
                for subpage_categori_class in sub_menu_soup.find_all('li',attrs = {'class' : 'filter_secondSub_title'}):
                    for link in subpage_categori_class.find_all('a'):
                        print("***href***: {}".format(link.get('href')))
                        sub_menu_url=link.get('href')
                        second_subcategories_name=sub_menu_url.split("/")[-1]
                        print("second_subcategories_name: {}".format(second_subcategories_name))
                        
                        subcategories_url="{}{}".format(main_url, sub_menu_url)
                        print("subcategories: {}".format(subcategories_url))
                        
                        #START calculate sub_page number 
                        req, sub_soup = select_page(subcategories_url)                
                        tt = sub_soup.find("div", {"id": "searchInfo"})                
                        val = float(tt.find('span').text)/12 # it has 12 product on each page
                        
                        val = Decimal(str(val))
                        page_number = int(Decimal(val.quantize(Decimal('1'),
                                                               rounding=ROUND_HALF_UP)))
                        
                        if page_number == 0: page_number = 1
                        #END calculate sub_page number 
               
                        for i in range(1, page_number + 1):
                            pages_subcategories_url="{}?sf={}".format(subcategories_url, i)
                            print("pages_subcategories_url: {}".format(pages_subcategories_url))
                            time.sleep(10)
                            seb_req, subpage_soup = select_page(pages_subcategories_url)
                            try:
                                image_link(subpage_soup, subcategories_name,second_subcategories_name)
                            except:
                                print("Hata Olustu")
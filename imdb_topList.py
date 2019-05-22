# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:10:58 2019
@author: betul
Bu kod imdb'nin en ünlü actor ve actresslerinin listesini cikarir.
"""

from bs4 import BeautifulSoup
import requests

def page_scraper(page_number):
    url ='https://www.imdb.com/search/name?gender=male,female&start={}&ref_=rlm'.format(page_number)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    divlist = soup.findAll('h3', {'class':'lister-item-header'})
    actList=[]
    for tr in divlist:
        actName = tr.findNext('a').text
        actList.append(actName)
#    print(actList)
    write_list_text_file(actList)
    page_number+=50
    page_scraper(page_number)

def write_list_text_file(actList):
    with open('ImdbTopList.txt', 'a') as f:
        for item in actList:
#            print(item)
            try:
                f.write("%s\n" % item)
            except Exception as ex:
                print(ex)
                f.write("%s\n" % item.encode('utf-8'))
    
if __name__ == '__main__':
    page_number=1
    page_scraper(page_number)
    
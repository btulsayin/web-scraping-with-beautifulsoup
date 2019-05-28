from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests,os

def page_scraper(page_number):
    if (page_number < 201):
        url ='https://www.imdb.com/search/name?gender=male,female&start={}&ref_=rlm'.format(page_number)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text)
        divlist = soup.findAll('div', {'class':'lister-item-image'})
        actList=[]
        f = open('links.txt', 'a')
        for tr in divlist:
            act = tr.find_all("img", src=True)
            actLink = str(act[0]['src'])
            actName = str(act[0]['alt']).replace(' ','_')
            save_image(actLink,actName)
            f.write(str(actName[0]['src']))
            f.write("\n")
            actList.append(act[0]['src'])

        page_number+=50
        page_scraper(page_number)
        
#resimleri istenilen klasöre indirmek için 
def save_image(imgUrl,image_name):
    try:
        #kaydedilmek istenen klasörün yolu belirtilir.        
        filePath = os.path.join("imdb", image_name+".jpg")
        print("filePath: {}".format(filePath))
        try:
            imgData = urlopen(imgUrl).read()
            output = open(filePath,'wb')
            output.write(imgData)
            output.close()
        except:
            print("Kaydedilemedi...")
    except Exception as ex:
        print("***Hata Olustu***{}".format(ex))        

    
if __name__ == '__main__':
    page_number=1
    page_scraper(page_number)
    
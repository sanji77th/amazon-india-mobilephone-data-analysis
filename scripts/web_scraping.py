from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


class urlSetter():

    def __init__(self):
        self.URLs = []

    def set_urls(self):
        num_of_pages = 20
        for page_counter in range(num_of_pages):
            page_num = page_counter + 1
            url = "https://www.amazon.in/s?k=mobile+phones&page={page_num}&crid=11V5A94MBOGZH&qid=1691473029&sprefix=mobile+phones%2Caps%2C644&ref=sr_pg_{page_num}".format(page_num=page_num)
            self.URLs.append(url)

    def get_urls(self):
        return self.URLs

class webScrapper():
    def __init__(self):
        self.data_dictionary = []
        self.HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    def scrape_data(self,URLs):
        for url_count in range(2):
            URL = URLs[url_count]
            webpage = requests.get(URL, headers=self.HEADERS)
            print(webpage)
            soup = BeautifulSoup(webpage.content, "html.parser")
            links = soup.find_all("a",attrs="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
            for link in links:
                self.scrape_single_data(link)
            #print(link)

    def scrape_single_data(self,link):
        '''
        URL = URLs[4]
        HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
        webpage = requests.get(URL, headers=HEADERS)
        print(webpage)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a",attrs="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        '''
        product_URL = "https://www.amazon.in" + link.get("href") 
        #print(product_URL)

        product_webpage = requests.get(product_URL, headers=self.HEADERS)
        page_soup = BeautifulSoup(product_webpage.content, "html.parser")

        def value_checker(value):
            if value==None:
                return "None"
            else:
                return value.text.strip()
            
        def secondary_value_checker(value, secondary_tag, secondary_attr):
            if value==None:
                return "None"
            else:
                return value.find(secondary_tag, attrs=secondary_attr).text.strip()
            
        title = value_checker(page_soup.find("span",attrs={'id':'productTitle'}))
        store = value_checker(page_soup.find("a", attrs={'id':'bylineInfo'}))
        rating = value_checker(page_soup.find("span", attrs="a-icon-alt"))
        number_of_ratings = value_checker(page_soup.find("span", attrs={'id':'acrCustomerReviewText'}))
        price = value_checker(page_soup.find("span", attrs="a-price-whole"))
        color = value_checker(page_soup.find("span", attrs={'id':'inline-twister-expanded-dimension-text-color_name'}))
        size = value_checker(page_soup.find("span", attrs={'id':'inline-twister-expanded-dimension-text-size_name'}))
        brand = secondary_value_checker(page_soup.find("tr", attrs="a-spacing-small po-brand"),"span","a-size-base po-break-word")
        model = secondary_value_checker(page_soup.find("tr", attrs="a-spacing-small po-model_name"),"span","a-size-base po-break-word")
        network = secondary_value_checker(page_soup.find("tr", attrs="a-spacing-small po-wireless_provider"),"span","a-size-base po-break-word")
        OS = secondary_value_checker(page_soup.find("tr", attrs="a-spacing-small po-operating_system"),"span","a-size-base po-break-word")
        cellular = secondary_value_checker(page_soup.find("tr", attrs="a-spacing-small po-cellular_technology"),"span","a-size-base po-break-word")
        
        #print(size)

        self.collect_data(title,store,rating,number_of_ratings,price,color,size,brand,model,network,OS,cellular)
        
    def collect_data(self,title,store,rating,number_of_ratings,price,color,size,brand,model,network,OS,cellular):
        data_row = {'title':title,
                    'store':store, 
                    'rating':rating, 
                    'number_of_ratings':number_of_ratings,
                    'price': price,
                    'color': color,
                    'size': size,
                    'brand': brand,
                    'model': model,
                    'network': network,
                    'OS': OS,
                    'cellular': cellular,
                    }
        self.data_dictionary.append(data_row)
        print("data record has been added!")

    def get_data(self):
        return self.data_dictionary
    
    def save_data_json(self):
        jsonString = json.dumps(self.data_dictionary)
        jsonFile = open("data/raw_data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

if __name__=="__main__":
    url_setter = urlSetter()
    url_setter.set_urls()
    URLs = url_setter.get_urls()
    #print(URLs[19])

    web_scrapper = webScrapper()
    web_scrapper.scrape_data(URLs)
    web_scrapper.save_data_json()
    
import requests
from bs4 import BeautifulSoup
import random
#quantity = 6   ## Replace it   ==========================
name_list = list()
price_list = list()
rating_list = list()
itemurl = list()
offer_list = list()
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
#                "Accept-Encoding": "gzip, deflate",
#                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
#                "Connection": "close", "Upgrade-Insecure-Requests": "1"}
def GET_UA():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0", \
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko", \
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0", \
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36" \
        ]

    return random.choice(uastrings)
class Scrapper_amazon():
    URL = 'https://www.amazon.in/s?k='

    def __init__(self, searchterm):
        # self.quantity = quantity   ## Replace it   ==========================
        self.name_list = list()
        self.specs_list = list()
        self.price_list = list()
        self.rating_list = list()
        self.item_url = list()
        self.img_url = list()
        self.offer_list = list()
        self.URL = self.URL + self.create_url(searchterm)
        self.headers = {'User-Agent': GET_UA()}
        self.response = requests.get(self.URL, headers=self.headers)
        self.soup = BeautifulSoup(self.response.content, 'lxml')

    def create_url(self, searchterm):
        string_list = searchterm.split(' ')
        new_string = ''
        for i in string_list:
            new_string = new_string + i + '+'
        return new_string[:-1]+'&page=1'

    def initialize(self):
        for d in self.soup.findAll('div', attrs={
            'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28'}):
            if len(self.name_list) == 3:
                break
            if d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}) is  None:
                pass
            else:
                name = d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'}).get_text()
                self.name_list.append(name)

            if d.find('span', attrs={'class': 'a-price-whole'}) is not None:
                price = d.find('span', attrs={'class': 'a-price-whole'}).get_text()
                self.price_list.append(price)

            if d.find('span', attrs={'class': 'a-size-base'}) is None:
                pass
            else:
                rating = d.find('span', attrs={'class': 'a-size-base'}).get_text()
                self.rating_list.append(rating)

            if d.find('a', attrs={'class': 'a-link-normal a-text-normal'}) is None:
                pass
            else:
                url = d.find('a', attrs={'class': 'a-link-normal a-text-normal'}).get('href')
                url = "https://www.amazon.in"+url
                self.item_url.append(url)

        for image in self.soup.findAll('img',class_='s-image'):
            img = image.get('src')
            self.img_url.append(img)
        if len(self.img_url) !=0:
            self.img_url.pop(0)

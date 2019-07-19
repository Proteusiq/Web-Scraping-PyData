'''
Web Scraping Using Requests and BeautifulSoup
    Aim to show how we ought not ninja HTML
    Design to show common pattern that we do not have to follow as 
    Network offers discoverable APIs
    e.g. https://www.bilbasen.dk/api/newest?page=1&pagesize=100
'''

from collections import defaultdict
import re


from bs4 import BeautifulSoup
from requests import Session
import pandas as pd


class Bilbasen:

    def __init__(self, url=None, headers=None):
        
        session = Session()

        if url is None:
            self.BASE_URL = 'https://www.bilbasen.dk/brugt/bil'
        else:
            self.BASE_URL = url
        

        if headers is None:
            headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'),
                    'Content-Type': 'application/json'}

        session.headers.update(headers)

        self.session = session
        self.store = defaultdict(list)



    def get_page(self, page=1, params=None):
        '''Gather Data From Bilbasen
        '''
        
        if params is None:
            params = {'fuel': 0,
            'yearfrom': 0,
            'yearto': 0,
            'pricefrom': 0,
            'priceto': 10000000,
            'mileagefrom': -1,
            'mileageto': 10000001,
            'includeengroscvr': True,
            'includeleasing': True}

        params.update({'page': page})

        

        r = self.session.get(self.BASE_URL, params=params)


        soup = BeautifulSoup(r.content, 'lxml')
        data = soup.find_all('div', class_='bb-listing-clickable')


        for item in data:
            car = item.find_all('div', class_=re.compile('col-xs'))
            try:
                #print(car[0].img['alt'])
                self.store['name'].append(car[0].img['alt'])
                self.store['desc'].append(
                    car[1].find('div', class_="listing-description"
                                ).get_text(strip=True))
                self.store['hk'].append(car[2].find_all('span')[0]['data-hk'])
                self.store['kml'].append(car[2].find_all('span')[0]['data-kml'])
                self.store['kmt'].append(car[2].find_all('span')[0]['data-kmt'])
                self.store['mont'].append(car[2].find_all('span')[0]['data-moth'])
                self.store['trailer'].append(car[2].find_all('span')[0]['data-trailer'])
                self.store['km_driven'].append(car[5].get_text(strip=True))
                self.store['model_year'].append(car[6].get_text(strip=True))
                self.store['price'].append(car[7].get_text(strip=True))

            except TypeError as e:
                # Problem: Data Not in the way we want
                #print(f'Problem: {e.__class__.__name__}')
                continue

            # Try-catch
            try:
                self.store['flag'].append(car[2].find_all('span')[1].get_text(strip=True))
            except IndexError:
                self.store['flag'].append('Sale')

        return self

    
if __name__ == '__main__':

    bils = Bilbasen()

    #data = bils.get_page(1).get_page(2)
    #df = pd.DataFrame(data.store)

    for page in range(1,5):
        bils.get_page(page)

    df = pd.DataFrame(bils.store)
    print(f'Data Stored {df.shape[0]} rows')
    print(f'Showing first 5 rows')
    print(df.head())

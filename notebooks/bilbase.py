'''
Just to discover https://www.bilbasen.dk/api/newest?page=1&pagesize=100
'''

from collections import defaultdict
import re


from bs4 import BeautifulSoup
from requests import Session
import pandas as pd

s = Session()
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'),
           'Content-Type': 'application/json'}

s.headers.update(headers)


BASE_URL = 'https://www.bilbasen.dk/brugt/bil'

PAGE_NR = 1
params = {'fuel': 0,
          'yearfrom': 0,
          'yearto': 0,
          'pricefrom': 0,
          'priceto': 10000000,
          'mileagefrom': -1,
          'mileageto': 10000001,
          'includeengroscvr': True,
          'includeleasing': True,
          'page': PAGE_NR}

store = defaultdict(list)


def get_data(url, params):
    '''Gather Data From Bilbasen
    '''
    r = s.get(url, params=params)


    soup = BeautifulSoup(r.content, 'lxml')
    data = soup.find_all('div', class_='bb-listing-clickable')


    for item in data:
        car = item.find_all('div', class_=re.compile('col-xs'))
        # print(car[0].img['alt'])
        store['name'].append(car[0].img['alt'])
        store['desc'].append(
            car[1].find('div', class_="listing-description"
                        ).get_text(strip=True))
        store['hk'].append(car[2].find_all('span')[0]['data-hk'])
        store['kml'].append(car[2].find_all('span')[0]['data-kml'])
        store['kmt'].append(car[2].find_all('span')[0]['data-kmt'])
        store['mont'].append(car[2].find_all('span')[0]['data-moth'])
        store['trailer'].append(car[2].find_all('span')[0]['data-trailer'])
        store['km_driven'].append(car[5].get_text(strip=True))
        store['model_year'].append(car[6].get_text(strip=True))
        store['price'].append(car[7].get_text(strip=True))

        # Try-catch
        try:
            store['flag'].append(car[2].find_all('span')[1].get_text(strip=True))
        except IndexError:
            store['flag'].append('Sale')

        return store

df = pd.DataFrame(store)

print(df.head())

# print(store)

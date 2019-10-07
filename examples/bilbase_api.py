
'''
Web Scraping Using Requests
    Aim to show how to use only requests and pandas (No need to ninja HTML)
    Design to show new pattern that we can follow 
    Using API found in Network
    e.g. https://www.bilbasen.dk/api/newest?page=1&pagesize=100
'''

from requests import Session
import pandas as pd


class Bilbasen:

    def __init__(self, url=None, headers=None):
        
        session = Session()

        if url is None:
            self.BASE_URL = 'https://www.bilbasen.dk/api/newest'
        else:
            self.BASE_URL = url
        

        if headers is None:
            headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'),
                    'Content-Type': 'application/json'}

        session.headers.update(headers)

        self.session = session
        self.store =  pd.DataFrame()



    def get_page(self, page=1, pagesize=100):
        '''Gather Data From Bilbasen
        '''
        
        params = {'page':page,
                 'pagesize':pagesize}

        r = self.session.get(self.BASE_URL, params=params)

        if r.ok:
            data = r.json()
            self.store = self.store.append(
                    pd.DataFrame(data.get('items')))

        else:
            self.store

        return self

        
    
if __name__ == '__main__':

    bils = Bilbasen()
    
    for page in range(1,5):
        bils.get_page(page)

    df = pd.DataFrame(bils.store)
    print(f'Data Stored {df.shape[0]} rows')
    print(f'Showing first 5 rows')
    print(df.head())

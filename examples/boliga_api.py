'''
Using Network on Chrome or Firefox, you can APIs for most of bolig sites
see bolig_network.py
'''

from requests import Session

class Boliga:
    '''Get Data From Boliga.dk API
    '''

    def __init__(self,job='sell'):

        # TODO:
        #   - Generate headers with fake_it
        #   - job defines what URL to call

        URL_STORE = {'sell': 'https://api.boliga.dk/api/v2/search/results',
                     'sold': 'https://api.boliga.dk/api/v2/sold/search/results',

        }
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/75.0.3770.80 Safari/537.36'}
        
        self.session = Session()
        self.session.headers.update(headers)

        self.url = URL_STORE[job]
        self.job = job
    
    def __repr__(self):
        return f"Boliga(job='{self.job}')"

    def get_data(self,params=None):
        'Get Data'
        # if prams is None, get default
        if params is None and self.job == 'sell':
            params = {'page': 1, 'pageSize':200}
        else:
            params = {'searchTab': 1, 'sort': 'date-d'}

        return self.session.get(self.url, params=params)
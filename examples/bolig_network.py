'''
One Function to Rule them all
Example of using Network to capture real Denmark's estate data
Simple modification to get more pages
Note: Use for educational purposes only
'''

import pandas as pd
from requests import Session

s = Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/75.0.3770.80 Safari/537.36'}
# Add headers
s.headers.update(headers)

# On Network check Preserve Logs, Disable Cache and XHR
# Perform a general search and observe the logs. Clear log
# and go to next page or load more estates

def get_data(url, method='get',**kwargs):
    
    req = {'get': s.get(url, **kwargs),
          'post': s.post(url,**kwargs)
          }
             
    res = req[method]
    print(f'Data from: {url}')
    return res.json()

# abc_data are for post and abc_params are for get calls

# Home.dk

HOME_URL = 'https://home.dk/umbraco/backoffice/home-api/Search'
home_params = {
    'CurrentPageNumber': 0,
    'SearchResultsPerPage': 45,
    'SearchType': 0
}

data = get_data(url=HOME_URL,params=home_params)
home_df = pd.DataFrame(data['searchResults'])
print(home_df.head(3))

# Nybolig & Estate get data from same source
NYBOLIG_URL = 'https://www.nybolig.dk/Services/PropertySearch/Search'
nybolig_data = {
    'isRental': False,
    'mustBeSold': False,
    'mustBeInProgress': False,
    'siteName': 'Nybolig',
    'take': 24,
    'skip': 0,
    'sort': 0
}

data = get_data(url=NYBOLIG_URL, method='post', data=nybolig_data)
nybolig_df = pd.DataFrame(data['Results'])
print(nybolig_df.head(3))

ESTATE_URL = 'https://www.estate.dk/Services/PropertySearch/Search'
estate_data = {
    'isRental': False,
    'mustBeSold': False,
    'mustBeInProgress': False,
    'siteName': 'Estate',
    'take': 100,
    'skip': 0,
    'sort': 0
}

data = get_data(url=ESTATE_URL, method='post', data=estate_data)
estate_df = pd.DataFrame(data['Results'])
print(estate_df.head(3))

#boligportal
#https://www.boligportal.dk/RAP/ads?startRecord=50

# Realmaeglerne.dk

REAL_URL = 'https://www.realmaeglerne.dk/Default.aspx'
real_params = {
    'ID': 10287,
    'refpageid': 10291,
    'search': '',
    'PageNum': 1,
    'PageSize': 100
}

data = get_data(url=REAL_URL, params=real_params)
real_df = pd.DataFrame(data['Boliger'])
print(real_df.head(3))


# MMLiving and Livingday

MML_URL = 'https://www.mmliving.dk/request/caselist/'
mml_params = {
    'limit': 3000,
    'salg': 1,
    'lege': 1,
    'solgt': 0
}

data = get_data(url=MML_URL, params=mml_params)
mml_df = pd.DataFrame(data).T
print(mml_df.head(3))

LIV_URL = 'https://livingday.dk/request/caselist/'
liv_params = {
    'start': 0, 
    'limit': 3000, 
    'salg': 1, 
    'leje': 1, 
    'investering': 1, 
    'sort': 'created_on',
    'sort_order': 'desc',
    'include_raw_dates':1,
    'solgt': 0, 
    'private': 1
}

data = get_data(url=LIV_URL, params=liv_params)
liv_df = pd.DataFrame(data)
print(liv_df.head(3))
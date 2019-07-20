'''
Progress Bar
Example of using progress bar for impatient miners like me
'''

import pandas as pd
from requests import Session

from tqdm import tqdm

s = Session()
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/75.0.3770.80 Safari/537.36'}
# Add headers
s.headers.update(headers)       

BOLIGA_URL = 'https://api.boliga.dk/api/v2/search/results' 

params = {'pageSize':200}
total_pages = 10

df = pd.DataFrame()

with tqdm(total=total_pages, 
        desc=f'Getting Boliga {params.get("pageSize")*total_pages} estates',
        bar_format='{l_bar}{bar} [time left: {remaining} ]') as pbar:
    
    for page in range(1, total_pages+1):
        
        params.update({'page': page})
        r = s.get(BOLIGA_URL, params=params)

        data = r.json()
        df = df.append(pd.DataFrame(data.get('results')))

        pbar.update(1)

print(f'Data Stored {df.shape[0]} rows')
print(f'Showing first 5 rows')
print(df.head())
from functools import wraps
from pathlib import Path
import random
import time
import sys

from loguru import logger
import pandas as pd
import requests



class Bolig:
    '''
    Alpha Project: Get Data From Bolighed.dk API with Python
    Usage:
    
    `python
    from bolighed import Bolig
    # Sleep between calls 5-15 seconds, get 500 at time, break_page 2
    bolig = Bolig(sleep(5,15), limit=500, break_page=2)
    bolig.mine
    `
    '''
 
    def __init__(self,sleep=(5,20),limit=500, break_page=None,
                    table_name='boligdata',location='data'):

        
        self.url = (f'https://bolighed.dk/api/external/market/propertyforsale/?'
                        f'limit={limit}')     
        self.break_page = break_page + 1
        self.min_wait, self.max_wait = sleep
        self.table_name= table_name
        self.location= location

        r = requests.get(self.url)
        if r.ok:
            logger.info('Connection to Bolighed.dk Successful')
            data = r.json()
        else:
            raise ConnectionError('Connection to Bolighed.dk Failed')
        
        self.count = data['count']
        self.pages = int(self.count/limit)
        self.limit = limit

        logger.info('Creating folder ./data and ./logs')

        [Path(loc).mkdir(parents=True, exist_ok=True) for 
            loc in [f'./{self.location}/','./logs/']]

        logger.add('./logs/bolig_{time}.log',compression='zip')
        logger.info(f'{self.count} estates found')
 
 
    def _get_bolighed_data(self): 
        r = requests.get(self.url)
        if r.ok:
            data = r.json()
        else:
            raise ConnectionError('Connection issue')
        return data['next'], pd.DataFrame(data['results'])

    @logger.catch
    def _build_bolighed_data(self):
        df = pd.DataFrame()
        logger.info(f'Start Loading: sleeping {self.min_wait} - {self.max_wait} seconds')
        page=1
        while self.url is not None:
            snooze = random.randint(self.min_wait, self.max_wait)
            logger.info(f'Page {page}|{self.pages}: Next sleep: {snooze} sec')
            self.url, df2 = self._get_bolighed_data()
            df = df.append(df2, ignore_index=True)
            page+=1
            time.sleep(snooze)
            if (self.break_page is not None) and (page == self.break_page):
                logger.info(f'Breaking at Page  {page-1}|{self.pages}')
                break
        return df
         

    @property
    def mine(self):
        logger.info(f'Gathering {self.count} estates. {self.limit} per page')
        df = self._build_bolighed_data()
        table_name= f"bolig_data_{pd.datetime.now().strftime('%Y%m%d')}"
        logger.info(f'loading to {df.shape[0]} estates into ./{self.location}/{table_name}.pkl.gz')
        df.to_pickle(f'./{self.location}/{table_name}.pkl.gz',compression='gzip')
        logger.info(f'File saved:./{self.location}/{table_name}.pkl.gz') 
        logger.info(f'Mining {df.shape[0]} estates completed')

if __name__ == '__main__':
    # Test: Get me bolig, sleep randomly between 5,20 sec
    # limit 500 bolig per page, and break at page 2
    bolig = Bolig(sleep=(5,20), limit=500, break_page=2)
    bolig.mine  
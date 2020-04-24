
'''
Web Scraping Using Requests
    Aim to show how to use only requests and pandas (No need to ninja HTML)
    Design to show new pattern that we can follow 
    Using API found in Network
    e.g. https://www.bilbasen.dk/api/newest?page=1&pagesize=100

This code is for educational purpose only. 
You MUST ask bilbasen permission to gather their data
'''

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from requests import Session
import numpy as np
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

    
    def __repr__(self):
        return f'Bilbasen(API={repr(self.BASE_URL)})'

    def get_page(self, page=1, pagesize=100, verbose=False):
        '''Gather Data From Bilbasen
            page:int page number
            pagesize:int number of cars in a page
            verbose:bool print mining progress
        '''
        
        params = {'page':page,
                 'pagesize':pagesize}
        

        r = self.session.get(self.BASE_URL, params=params)

        if r.ok:
            data = r.json()
            
            self.store = self.store.append(
                    pd.DataFrame(data.get('items')), ignore_index=True)

        else:
            self.store
            
        if verbose:
            print(f'[+] Gathering data from page {page:}.{" ":>5}Found {len(self.store):>5} cars'
                 f'{" ":>3}Time {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}')

        return self
    
    
    
    def get_pages(self, start_page=1, end_page=10, threads=3, verbose=False):
        '''
         Parallel Gathering Data From Bilbasen
            start_page:int page number to start
            end_pagee:int  page number to end
            threads:int number of workers
            verbose:bool print mining progress
        '''
        func = lambda pages: [self.get_page(page, verbose=verbose)for page in pages]
        
        max_pages = start_page + end_page + 1
        pages_split = np.array_split(np.arange(start_page,max_pages), threads)
        
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            _ = [executor.submit(func, split) for split in pages_split]
        
        return self
                

        
    
if __name__ == '__main__':

    bils = Bilbasen()
    
    # one call at a time
    print('[+] Start single thread calls\n')
    _ = [bils.get_page(page=page, pagesize=100, verbose=True) for page in range(1,5)]

    df = bils.store
    print(f'Data Stored {df.shape[0]} rows\n')
                  
    # multipe calls at once
    threads = 4
    print(f'[+] Start {threads} threads calls\n')
    bils.get_pages(start_page=5, end_page=15, threads=threads, verbose=True)
    print(f'Data Stored {bils.store.shape[0]} rows\n')

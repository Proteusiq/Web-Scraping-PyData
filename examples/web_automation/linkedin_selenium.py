'''
Simple way of using selenium to get LinkedIn Connection Name and Title
'''

from collections import defaultdict
import json
import logging
import os
import re
import time

from bs4 import BeautifulSoup, element as bs4_element
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import helpers

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

class LinkedIn:
    '''
    '''
    
    def __init__(self, snooze=2):

        self.login = False
        self.message_window_is_miminized = False
        logging.info('Setting Up LinkedIn')
        self.snooze = snooze

    def __repr__(self):
        
        if self.login:
            self._LinkedIn__my_profile()
            show = f'[On] LinkedIn({repr(self.my_name)})'
        else:
            show = '[Off] LinkedIn()'

        return show

        

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.driver.quit()
        self.login = False
        logging.info('Driver quit successful')


    def sign_in(self, username, password):

        try:
            assert username and password, 'Incorrect credentials'
        
        except AssertionError:
            logging.error('No credentials', exc_info=True)
            logging.info('Pass in Username and Password')

            # needed if all failed ask and place to session
            from getpass import getpass 
            username = input('Username: ')
            password = getpass('Password: ')

        logging.info('Login in LinkedIn')
        self.username = username
        self.password = password

        
        
        # Remove the Automation Info 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get('https://www.linkedin.com/login')
    
        user_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        user_name.clear()
        user_name.send_keys(self.username)
    
        user_pwd = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        user_pwd.clear()
        user_pwd.send_keys(self.password)
        user_pwd.submit()
        
        self.driver = driver
        self.login = True
        logging.info('Login Successful')

        return self
    
    def sign_off(self, soup=True):
        
        time.sleep(5)
        
        if soup:
            self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
            logging.info('Logoff with soup')
            
        self.driver.close()
        logging.info('Logoff Successful')
        self.login = False
        return self

    def __my_profile(self):
        '''Private function
        Note meant to be used outside class
        Get My Profiles Name, Info and Id
        '''

        pattern = re.compile('^bpr-guid-*')
        codes = helpers.driver_tags(self.driver, 
                                    search='find_all',
                                    query=('code',{'id':pattern}))
        data = [code.get_text(strip=True) for code in codes 
                if 'publicContactInfo' in code.get_text(strip=True)]

        mig = json.loads(data[-1])
        self.my_name = f"{mig['included'][0]['firstName']} {mig['included'][0]['lastName']}"
        self.my_info = mig['included'][0]['occupation']
        self.my_profile_id = mig['included'][0]['publicIdentifier']

        return self

    
    @property
    def connections(self):
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mynetwork-tab-icon'))
        ).click()

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'mn-community-summary__entity-info'))
        ).click()
        
        return self
    
    
    @property
    def scroll(self):

        KEEP_SCROLLING = True

        # Get current scrol height
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        
        logging.info('Scrolling in progress ...')
        print('\n[.', end='')
        while KEEP_SCROLLING:

            # Scroll down to bottom
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

            # Wait to load page
            time.sleep(self.snooze)

            # Get the new scrolled height
            scrolled_height = self.driver.execute_script("return document.body.scrollHeight")
            # Check if we should keep scrolling
            
            
            if scrolled_height == current_height:
                KEEP_SCROLLING = False
            current_height = scrolled_height
            print('.', end='', flush=True)
        print(']\n')
        
        logging.info('Scrolling Completed!')   
        return self

    @property    
    def  minimize_message_window(self):
    
        class_ = 'msg-overlay-bubble-header__button'
        msg_window = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, class_)))
        
        msg = msg_window.text
        
        if 'minimize' in msg:
            msg_window.click()
            logging.info('Message Window Minimized')
        else:
            logging.info('Message Window already minimized')

        self.message_window_is_miminized = True  
        return self

    @property    
    def  get_all_connections(self):
        
        total_connections = "search-results__total"
        connections_filter = "search-s-facet__form"
        clear_btn = "facet-collection-list__clear-button"
        apply_btn = "facet-collection-list__apply-button"

        try: 
            self.driver.find_elements_by_class_name(connections_filter)[0].click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, clear_btn))
                    ).click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, apply_btn))).click()
            logging.info('Getting all connections')
            self.all_connections = True
        
        except exceptions.NoSuchElementException:
            self.all_connections = True
            logging.info('Already have all connections')
            pass

        connection_num = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, total_connections))).text

        self.connection_total = int(connection_num.split()[1])
        self.pages = np.ceil(self.connection_total/10).astype(int)
        
        return self
    

class LinkedInSoup:
    ''' LinkedInSoup
     # TODO
    '''

    def __init__(self, driver, parser='lxml'):

        '''
        Return show image of element from selenium driver

        :param selenium driver: Selenium driver instance
        :param selenium element: Selenium element to focus

        :return: TODO
        
        :raises ValueError: Coming soon
        :raises TypeError: Coming soon
        '''
        
        soup = BeautifulSoup(
                driver.page_source, parser)
        self.soup = soup
        self.driver = driver
        self.store = defaultdict(list)
        
    def __repr__(self):
        
        show = ''
        if self.store:
            index = np.random.randint(0, len(self.store)+1, 5)
            names = [name for i,name in enumerate(self.store['profile_name']) if i in index]
            for name in names:
                show+=f".Node('{name}')"
                
        else:
            show = '.Node()'
        
        return show[1:]
        
    def prep_connection(self, image=False):

        section = self.soup.find('section',class_='mn-connections')
        connections = section.find_all('li', class_='list-style-none')
        logging.info(f'{len(connections)} connections found')
        
        for profile in connections:
            
            p = profile.find('a',{'data-control-name':'connection_profile'})
            self.store['profile_url'].append(p['href'])
            self.store['profile_name'].append(p.img['alt'])
            if image:                             
                self.store['profile_img_url'].append(p.img['src'])
            
            title = profile.find('span',class_='mn-connection-card__occupation').get_text(strip=True)
            self.store['title'].append(title)
            
        return self

    def get_profile_info(self, profile_url, parser='lxml'):
        
        self.driver.get(profile_url)
        
        codes = BeautifulSoup(
            self.driver.page_source,parser).find_all('code')
        
        try:
            data = [json.loads(code.get_text(strip=True)) for code in codes 
                if "*profile" in code.get_text(strip=True)][0]

            logging.info(f'{profile_url}: Profile info found')

            return data
        
        except IndexError:
            logging.warning(f'{profile_url}: Profile info not found')
            
 
    def get_profile_data(self, profile_url, parser='lxml'):
        
        self.driver.get(profile_url)
        
        codes = BeautifulSoup(
            self.driver.page_source,parser).find_all('code')
        
        try:
            data = [json.loads(code.get_text(strip=True)) for code in codes 
                if code.get_text(strip=True).startswith('{"data"')]

            logging.info(f'{profile_url}: {len(data)} chucks of profile data found')

            return data
        
        except IndexError:
            logging.warning(f'{profile_url}: No chucks of profile data found')

    def get_driver_data(self, driver, parser='lxml'):
        '''
        requires a current driver
        '''
        self.driver = driver
        
        codes = BeautifulSoup(
            self.driver.page_source,parser).find_all('code')
        
        try:
            data = [json.loads(code.get_text(strip=True)) for code in codes 
                if code.get_text(strip=True).startswith('{"data"')]

            logging.info(f'Codes Data: {len(data)} chucks of codes data found')

            return data
        
        except IndexError:
            logging.warning(f'Codes Data: No chucks of data found')



      

if __name__ == '__main__':
    
    user = os.environ.get('LINKEDIN_USER')
    pwd = os.environ.get('LINKEDIN_PWD')
    
    linkedin = LinkedIn(snooze=1)
    
    try:
        
        linkedin.sign_in(username=user,password=pwd)
        linkedin.connections.scroll
        
    finally:
        
        connections = LinkedInSoup(linkedin.driver)
        connections.prep_connection()
        linkedin.sign_off()
    
    
    df = pd.DataFrame(connections.store)
    
    print(df[['profile_name','title']].head())

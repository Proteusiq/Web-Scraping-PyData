'''
Simple way of using selenium to get LinkedIn Connection Name and Title
'''

from collections import defaultdict
import logging
import os
import time

from bs4 import BeautifulSoup, element as bs4_element
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

class LinkedIn:
    
    def __init__(self, snooze=2):
        
        logging.info('Setting Up LinkedIn')
        self.snooze = snooze
         

    def sign_in(self, username, password):
        logging.info('Login in LinkedIn')
        self.username = username
        self.password = password
        
        # Remove the Automation Info 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
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
        
        logging.info('Login Successful')
        return self
    
    def sign_off(self, soup=True):
        
        time.sleep(5)
        
        if soup:
            self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
            logging.info('Logoff with soup')
            
        self.driver.close()
        logging.info('Logoff Successful')
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

class LinkedInSoup:
    
    def __init__(self, soup):
        
        if not isinstance(soup, bs4_element.Tag):
            logging.error(f'Beautiful soup element required. {type(soup)} was given')
        self.soup = soup
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
        

if __name__ == '__main__':
    
    user = os.environ.get('LINKEDIN_USER')
    pwd = os.environ.get('LINKEDIN_PWD')
    
    linkedin = LinkedIn(snooze=1)
    
    try:
        
        linkedin.sign_in(username=user,password=pwd)
        linkedin.connections.scroll
        
    finally:
        
        linkedin.sign_off()
    
    connections = LinkedInSoup(linkedin.soup)
    
    connections.prep_connection()
    
    df = pd.DataFrame(connections.store)
    
    print(df[['profile_name','title']].head())

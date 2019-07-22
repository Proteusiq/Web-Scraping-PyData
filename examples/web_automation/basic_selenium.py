from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Remove the Automation Info 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-infobars")
driver = webdriver.Chrome(chrome_options=chrome_options)

URL = 'https://www.linkedin.com/'

try:
    driver.get(URL)
    driver.implicitly_wait(60)

finally:
    input('Press to Exit!')
    driver.close()
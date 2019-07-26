import io

from bs4 import BeautifulSoup
from PIL import Image


def driver_tags(driver, search, query, parser='lxml'):
    '''
    Return searched soup from selenium driver

    :param selenium driver: Selenium driver instance
    :param str search: 'find_all','find' are supported
    :param tuple query: tuple of tags e.g ('div',{'id':'3'})
    :param str parser: Beautifulsoup marker default=lxml
    :return: list or instance of Beautifulsoup soup
    
    :raises ValueError: Coming soon
    :raises TypeError: Coming soon
    '''

    soup = BeautifulSoup(driver.page_source, parser)

    methods = {
         'find_all': soup.find_all,
         'find': soup.find,
    }

    return methods[search](query)


def show_element(driver, element):
     '''
    Return show image of element from selenium driver

    :param selenium driver: Selenium driver instance
    :param selenium element: Selenium element to focus

    :return: None
    
    :raises ValueError: Coming soon
    :raises TypeError: Coming soon


    #TODO: Get size to decide which ember 43-45 
    '''
    
     location = element.location
     size = element.size
     _ = driver.get_screenshot_as_png()
     img = Image.open(io.BytesIO(_))
    
    # region of interest
     roi = (location['x'], 
           location['y'],
           location['x'] + size['width'], 
           location['y'] + size['height'])
    
     img = img.crop(roi)
     img.show()
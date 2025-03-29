import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Website_Scraper():
    
    def __init__(self, url):
        self.__url = url
        self.__links = []
    
    def __get_url(self):
        """
        Retrieves the current site url.
        """
        return self.__url
    
    def get_links(self):

        response = requests.get( self.__get_url() )
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Make sure everything is in absolute path :)
        self.__links = [
            urljoin(self.__url, link['href']) 
            for link in soup.find_all("a", href=True)
        ]
            
        return self.__links;
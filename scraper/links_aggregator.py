import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from intelligence.links_relevancy_analyzer import LinksRelevancyAnalyzer

class Website_Scraper():
    
    def __init__(self, url):
        self.__url = url
        self.__links = []
        self.__site_content = ""
    
    def get_url(self):
        """
        Retrieves the current site url.
        """
        return self.__url
    
    def get_links(self):

        response = requests.get( self.get_url() )
        soup = BeautifulSoup(response.text, "html.parser")
        # Make sure everything is in absolute path :)
        self.__links = [
            urljoin(self.__url, link['href']) 
            for link in soup.find_all("a", href=True)
        ]
            
        return self.__links;
    
    def get_title(self):
        
        response = requests.get( self.get_url() )
        soup = BeautifulSoup(response.text, "html.parser")
        
        title_tag = soup.title
        title = title_tag.string.strip() if title_tag and title_tag.string else "No title"
        
        return title
    
    def get_contents(self):
        
        response = requests.get( self.get_url() )
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        
        return text

    def get_summary(self):
        
        result = "Landing page:\n"
        result += self.get_contents()
        
        links_analyzer = LinksRelevancyAnalyzer( self.get_links(), self.get_url() )
        links = links_analyzer.analyze()
        
        print("Scanning links");
        for link in links["links"]:
            result += f"\n\n{link['type']}\n"
            result += Website_Scraper(link["url"]).get_contents()
        return result
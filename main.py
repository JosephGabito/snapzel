from scraper.links_aggregator import Website_Scraper
from intelligence.links_relevancy_analyzer import Links_Relevancy_Analyzer

def main():
    website = Website_Scraper('https://automatorplugin.com')
    links   = website.get_links()
    
    links_analyzer = Links_Relevancy_Analyzer( links )
    print( links_analyzer.get_links() )
    pass

main()
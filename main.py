from scraper.links_aggregator import Website_Scraper
from intelligence.links_relevancy_analyzer import LinksRelevancyAnalyzer
from dotenv import load_dotenv

load_dotenv()

def main():
    url = "https://automatorplugin.com";

    website = Website_Scraper( url )
    links   = website.get_links()
    
    links_analyzer = LinksRelevancyAnalyzer( links, url )
    print( links_analyzer.analyze() )

main()
from scraper.links_aggregator import Website_Scraper
from intelligence.links_relevancy_analyzer import Links_Relevancy_Analyzer

def main():
    url = "https://automatorplugin.com";

    website = Website_Scraper( url )
    links   = website.get_links()
    
    links_analyzer = Links_Relevancy_Analyzer( links, url )
    print( links_analyzer.get_user_prompt() )
    pass

main()
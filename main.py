from scraper.links_aggregator import Website_Scraper

def main():
    website = Website_Scraper('https://automatorplugin.com')
    print( website.get_links() )
    pass

main()
from scraper.links_aggregator import Website_Scraper
from openai import OpenAI
from IPython.display import Markdown, display, update_display

class Summary_Analyzer:
    
    def __init__(self, website:Website_Scraper):
        self.__website = website
        self.__system_prompt = (
            "You are an assistant that analyzes the contents of several relevant pages from a company website \
            and creates a short humorous, entertaining, jokey brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
            Include details of company culture, customers and careers/jobs if you have the information."
        )
        
    def get_user_prompt(self):
        user_prompt = f"You are looking at a company called: {self.__website.get_title()}\n"
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += self.__website.get_summary()
        user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
        return user_prompt
    
    def create_brochure(self):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.__system_prompt},
                {"role": "user", "content": self.get_user_prompt()}
            ],
        )
        result = response.choices[0].message.content
        return result
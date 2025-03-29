from openai import OpenAI

class Links_Relevancy_Analyzer():
    
    def __init__(self,links:list, url):
        self.__links = links
        self.__url = url
        pass
    
    def get_links(self):
        return ("\n").join( self.__links )
    
    def get_system_prompt(self):
        prompt = "You are provided with a list of links found on a webpage.\
You are able to decide which of the links would be most relevant to include in a brochure about the company,\
such as links to an About page, or a Company page, or Careers/Jobs pages \
You should response in JSON as in this example:"

        prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
        """
        
        return prompt
    
    def get_user_prompt(self):
        
        user_prompt = f"Here is the list of links on the website of {self.__url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += f"\n {self.get_links()}"
        
        return user_prompt

    pass
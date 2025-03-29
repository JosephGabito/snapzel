import json
from openai import OpenAI

class LinksRelevancyAnalyzer:
    def __init__(self, links: list, url: str):
        self.__links = links
        self.__url = url

    def get_links(self) -> str:
        """
        Returns the list of links joined by newline.
        """
        return "\n".join(self.__links)

    def get_system_prompt(self) -> str:
        """
        Returns the system prompt for OpenAI that instructs the model how to interpret the links.
        """
        return (
            "You are provided with a list of links found on a webpage. "
            "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
            "such as links to an About page, or a Company page, or Careers/Jobs pages. "
            "You should respond in JSON as in this example:\n\n"
            "{\n"
            '    "links": [\n'
            '        {"type": "about page", "url": "https://full.url/goes/here/about"},\n'
            '        {"type": "careers page", "url": "https://another.full.url/careers"}\n'
            "    ]\n"
            "}"
        )

    def get_user_prompt(self) -> str:
        """
        Returns the user prompt that contains the actual list of links and instructions for analysis.
        """
        return (
            f"Here is the list of links on the website of {self.__url} - "
            "please decide which of these are relevant web links for a brochure about the company. "
            "Respond with the full https URL in JSON format. "
            "Do not include Terms of Service, Privacy Policy, or email links.\n\n"
            "Links:\n"
            f"{self.get_links()}"
        )
        
    def analyze(self):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": self.get_user_prompt()}
        ],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)

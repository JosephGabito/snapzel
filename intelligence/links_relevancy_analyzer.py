from openai import OpenAI

class Links_Relevancy_Analyzer():
    
    def __init__(self,links:list):
        self.__links = links
        pass
    
    def get_links(self):
        return self.__links
    pass
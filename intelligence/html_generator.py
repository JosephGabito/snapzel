from openai import OpenAI

class HTMLGenerator():
    
    def __init__(self,md_contents):
        
        self.__system_prompt = "You are an expert HTML/CSS developer. Convert the given Markdown into a modern, responsive landing page using only semantic HTML5 and internal CSS—no external assets, no explanations, and no extra content before or after the root HTML element."
        
        self.__user_prompt = f"I want you to turn this into beautiful and modern landing page. {md_contents}"
    
    def generate_landing_page_html(self):
        
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.__system_prompt},
                {"role": "user", "content": self.__user_prompt}
            ],
        )

        result = response.choices[0].message.content
        
        return self.strip_code_fence( result )
    
    def strip_code_fence(self,content: str) -> str:
        lines = content.strip().splitlines()
        if lines[0].startswith("```"):
            return "\n".join(lines[1:-1])
        return content
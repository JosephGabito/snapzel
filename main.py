import os
import uuid
import markdown
from dotenv import load_dotenv
from scraper.links_aggregator import Website_Scraper
from intelligence.summary_analyzer import Summary_Analyzer
from intelligence.html_generator import HTMLGenerator
from html_sanitizer import Sanitizer
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hey folks": "I'm here"}

def service():
    url = "https://uncannyowl.com/"
    session_id = str(uuid.uuid4())
    session_dir = "temp"
    os.makedirs(session_dir, exist_ok=True)

    scraper = Website_Scraper(url)
    summary_analyzer = Summary_Analyzer(scraper)
    markdown_content = summary_analyzer.create_brochure()

    md_path = os.path.join(session_dir, f"brochure-{session_id}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    gen = HTMLGenerator(markdown_text)
    content = gen.generate_landing_page_html()

    with open('temp/landing.html', "w", encoding="utf-8") as f:
        f.write(content)

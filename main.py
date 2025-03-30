import os
import time
import validators

from fastapi import FastAPI,HTTPException
from app.celery_worker import generate_brochure_task
from dotenv import load_dotenv

load_dotenv()

print(f"[FASTAPI] REDISCLOUD_URL = {os.getenv('REDISCLOUD_URL')}")

app = FastAPI()

"""
Requests to Root
"""
@app.get("/")
@app.post("/")
def root():
    return {"_ts": time.time()}

"""
POST request to /generate endpoint.
"""
@app.post("/generate")
def generate(data: dict):
    
    url = data.get("url")
    validate = validators.url( url )
    
    if url is None:
        raise HTTPException(status_code=400, detail=f"Key 'url' is required in the dictionary")
    if True != validate:
        raise HTTPException(status_code=400, detail=f"{url} is not a valid url")

    task = generate_brochure_task.delay(url)
    
    return {"task_id": task.id}

"""
GET request to /generate endpoint.
"""
@app.get("/status/{task_id}")
def status(task_id: str):
    from app.celery_worker import celery
    result = celery.AsyncResult(task_id)
    return {
        "state": result.state,
        "result": result.result
    }
"""
@app.get("/create-service")
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
"""
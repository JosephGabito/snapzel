from celery import Celery
from dotenv import load_dotenv

from app.repository.database_instance import db

from intelligence.html_generator import HTMLGenerator
from intelligence.summary_analyzer import Summary_Analyzer
from intelligence.summary_analyzer import Website_Scraper

import os

load_dotenv()

redis_url = os.getenv("REDISCLOUD_URL")
env = os.getenv("ENV", "dev")  # "prod" or "dev" (default to "dev")

print(f"[CELERY] REDISCLOUD_URL = {redis_url}")
print(f"[CELERY] ENV = {env}")

celery = Celery("tasks", broker=redis_url)

# Base config
celery.conf.update(
    broker_pool_limit=5,              # Safe number for upgraded Redis
    worker_concurrency=5,             # Process 5 tasks in parallel
    task_acks_late=True,              # Retry if worker dies mid-task
    worker_prefetch_multiplier=1,     # Prevent task hoarding
    broker_heartbeat=10,              # Keep Redis connections alive
    broker_connection_timeout=30,     # Avoid infinite hangs
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600               # Cleanup after 1 hour
)

# Result backend config (only enable in non-prod)
if env != "prod":
    celery.conf.update(
        task_ignore_result=False,
        result_backend=redis_url
    )
else:
    celery.conf.update(
        task_ignore_result=True,
        result_backend=None
    )
    
def generate_brochure(url:str, user_id:str):
    
    session_dir = "temp"
    os.makedirs(session_dir, exist_ok=True)

    scraper = Website_Scraper(url)
    summary_analyzer = Summary_Analyzer(scraper)
    markdown_content = summary_analyzer.create_brochure()

    # Create the Markdown.
    md_path = os.path.join(session_dir, f"brochure-{user_id}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # Reads the Markdown.
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # Tap into HTMLGenerator and pass the Markdown text.
    gen = HTMLGenerator(markdown_text)
    content = gen.generate_landing_page_html()

    # Finally convert it to HTML
    with open(f"temp/landing-{user_id}.html", "w", encoding="utf-8") as f:
        f.write(content)


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def generate_brochure_task(self, url: str):

    print(f"🚀 Generating brochure for {url} with task id of {self.request.id}")

    jobs_collection = db.get_collection('jobs')
    jobs_collection.update_one(
        {"task_id": self.request.id},
        {"$set": {"status": "in-progress"}}
    );

    generate_brochure( url, self.request.id )

    jobs_collection.update_one(
        {"task_id": self.request.id},
        {"$set": {"status": "done"}}
    );
    
    return f"✅ Brochure generated for {url}"

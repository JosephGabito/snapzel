from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ This is what's missing!

redis_url = os.getenv("REDISCLOUD_URL")
print(f"[CELERY] REDISCLOUD_URL = {redis_url}")

celery = Celery("tasks", broker=redis_url, backend=redis_url)

@celery.task
def generate_brochure_task(url: str):
    import time
    print(f"Generating brochure for {url}")
    time.sleep(10)
    return f"✅ Brochure generated for {url}"

from celery import Celery

import os

# Redis connection (Heroku or local)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

celery = Celery("tasks", broker=redis_url, backend=redis_url)

@celery.task
def generate_brochure_task(url: str):
    import time
    print(f"Generating brochure for {url}")
    time.sleep(10)  # simulate AI work
    return f"✅ Brochure generated for {url}"

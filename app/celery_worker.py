from celery import Celery
from dotenv import load_dotenv
from app.repository.database_instance import db

import os
import time

load_dotenv()

redis_url = os.getenv("REDISCLOUD_URL")
env = os.getenv("ENV", "dev")  # "prod" or "dev" (default to "dev")

print(f"[CELERY] REDISCLOUD_URL = {redis_url}")
print(f"[CELERY] ENV = {env}")

celery = Celery("tasks", broker=redis_url)

# Base config
celery.conf.update(
    broker_pool_limit=5,              # 🧠 Safe number for upgraded Redis
    worker_concurrency=2,             # 🔄 Process 2 tasks in parallel
    task_acks_late=True,              # ✅ Retry if worker dies mid-task
    worker_prefetch_multiplier=1,     # 🧹 Prevent task hoarding
    broker_heartbeat=10,              # ❤️ Keep Redis connections alive
    broker_connection_timeout=30,     # ⏳ Avoid infinite hangs
    broker_connection_retry_on_startup=True,
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600               # 🕓 Cleanup after 1 hour
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

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def generate_brochure_task(self, url: str):
    print(f"🚀 Task ID: {self.request.id}")
    print(f"🚀 Generating brochure for {url}")
    
    jobs_collection = db.get_collection('jobs')
    jobs_collection.update_one({
        {"task_id": self.request.id},
        {"$set": {"status": "in-progress"}}
    });
    
    time.sleep(45)  # Simulate processing

    jobs_collection.update_one({
        {"task_id": self.request.id},
        {"$set": {"status": "done"}}
    });
    
    return f"✅ Brochure generated for {url}"

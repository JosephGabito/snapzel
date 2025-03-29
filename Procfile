web: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT 
worker: celery -A app.celery_worker.celery worker --loglevel=info

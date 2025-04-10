import os
import time
import json
import validators

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from clerk_backend_api import Clerk
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions

from app.celery_worker import generate_brochure_task

# Load environment variables
load_dotenv()

print(f"[FASTAPI] REDISCLOUD_URL = {os.getenv('REDISCLOUD_URL')}")

# Initialize FastAPI
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://snapzel-clerk.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Clerk Auth Dependency
# -----------------------------
def get_authenticated_user(request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        sdk = Clerk(bearer_auth=os.getenv('CLERK_SECRET_KEY'))

        request_state = sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["https://snapzel-clerk.vercel.app", "http://localhost:3000"]
            ),
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="User is not authenticated")

        return request_state.payload

    except Exception as error:
        try:
            error_dict = json.loads(str(error))
            message = error_dict.get("errors", [{}])[0].get("long_message", str(error))
        except json.JSONDecodeError:
            message = str(error)
        raise HTTPException(status_code=401, detail=message)


# -----------------------------
# Routes
# -----------------------------
@app.get("/")
@app.post("/")
def root(): 
    """
    Root url.
    """
    return {
       "_ts": time.time(),
    }
   

@app.post("/generate")
def generate(data: dict, request: Request, user=Depends(get_authenticated_user)):
    """
    Generate brochures.
    """
    url = data.get("url")

    if not url:
        raise HTTPException(status_code=400, detail="Key 'url' is required")
    if not validators.url(url):
        raise HTTPException(status_code=400, detail=f"{url} is not a valid URL")

    task = generate_brochure_task.delay(url)

    from app.repository.database_instance import db
    
    document = {
        "url": url,
        "task_id": task.id,
        "status": "pending",
        "user_id_clerk": user['user_id'],
        "date_added": time.time()
    }

    jobs_collection = db.get_collection('jobs')
    jobs_collection.insert_one( document )

    return {"task_id": task.id}

@app.get("/status/{task_id}")
def status(task_id: str):
    
    from app.celery_worker import celery
    result = celery.AsyncResult(task_id)

    return {
        "state": result.state,
        "result": result.result
    }

@app.get("/user/tasks")
def find_user_tasks(user=Depends(get_authenticated_user)):
    from app.repository.database_instance import db
    from pymongo import DESCENDING

    jobs_collection = db.get_collection("jobs")
    jobs = jobs_collection.find({
        "user_id_clerk": user['user_id'],
        "date_added": {"$exists": True }
    }).sort("date_added", DESCENDING )
    
    tasks = []
    
    for job in jobs:
        job['_id'] = str( job['_id'] )
        tasks.append( job )
    
    return {
        "tasks": tasks
    }

def serve_file(file_prefix: str, file_extension: str, file_type: str, task_id: str):
    from fastapi.responses import FileResponse  # Local import (intentional + clean)

    # Define the file path
    filename = f"{file_prefix}-{task_id}.{file_extension}"
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    file_path = os.path.join(temp_dir, filename)

    # Check existence
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    # Serve the file
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=file_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# -------------------------
# Endpoint: README (Markdown)
# -------------------------
@app.post("/download-readme")
async def download_readme(data: dict, user=Depends(get_authenticated_user)):
    task_id = data.get("task_id")
    if not task_id:
        raise HTTPException(status_code=400, detail="Missing task_id")

    return serve_file("brochure", "md", "text/markdown", str(task_id))


# -------------------------
# Endpoint: Landing Page (HTML)
# -------------------------
@app.post("/download-landing-page")
async def view_landing(data: dict, user=Depends(get_authenticated_user)):
    task_id = data.get("task_id")
    if not task_id:
        raise HTTPException(status_code=400, detail="Missing task_id")

    return serve_file("landing", "html", "text/html", str(task_id))

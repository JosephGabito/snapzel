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
    return {"task_id": task.id}

@app.get("/status/{task_id}")
def status(task_id: str):
    
    from app.celery_worker import celery
    result = celery.AsyncResult(task_id)

    return {
        "state": result.state,
        "result": result.result
    }

# -----------------------------
# Archived Route (Keep for Reference)
# -----------------------------

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

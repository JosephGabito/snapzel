import os

from app.repository.database import Database
from dotenv import load_dotenv
load_dotenv()

db = Database( os.getenv('MONGO_SRV') )  # Use env vars in real projects

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    APP_NAME = "LLM Platform"
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")  # Default MongoDB URL
    MYSQL_URL = os.getenv("MYSQL_URL", "mysql://user:password@localhost/dbname")  # Default MySQL URL

config = Config()

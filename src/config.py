import os

from dotenv import load_dotenv

load_dotenv(override=True)


POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

import os
from dotenv import load_dotenv

SECRETS_FILE = os.getenv("AUTH_SECRETS_FILE", ".env")
load_dotenv(SECRETS_FILE)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
import os
from dotenv import load_dotenv

SECRETS_FILE = os.getenv("DISCORD_SECRETS_FILE", ".env")
load_dotenv(SECRETS_FILE)

ALLOWED_SERVERS = [int(server_id) for server_id in os.getenv("ALLOWED_SERVERS", "").split(",")]
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

CLIENT_ID = int(os.getenv("OSU_CLIENT_ID", -1))
CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_SERVICE_ACCOUNT_CREDS_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDS_FILE")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "")
GOOGLE_SHEET_CELL_RANGE = os.getenv("GOOGLE_SHEET_CELL_RANGE", "")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_SERVER = os.getenv("EMAIL_SERVER", "")
MAX_AUTH_SESSIONS = int(os.getenv("MAX_AUTH_SESSIONS", 5))

AUTH_CODE_LEN = int(os.getenv("AUTH_CODE_LEN", 15))
AUTH_CODE_DURATION = int(os.getenv("AUTH_CODE_DURATION", 5))

CWS_ROLE_ID = int(os.getenv("CWS_ROLE_ID", -1))

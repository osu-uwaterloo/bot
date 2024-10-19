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
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "")
GOOGLE_SHEET_CELL_RANGE = os.getenv("GOOGLE_SHEET_CELL_RANGE", "")
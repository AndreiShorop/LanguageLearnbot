import os
import sys
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    sys.exit("ERROR: BOT_TOKEN is not set. Add it to your .env file.")

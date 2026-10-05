import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN_TG_BOT")
if not TOKEN:
    raise ValueError("TOKEN_TG_BOT variable is missing inside your .env file!")
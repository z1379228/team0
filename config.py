import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

guild_id = os.getenv("GUILD_ID")
GUILD_ID = int(guild_id) if guild_id else None

DATABASE = "database/teambot.db"

PLAYER_FOLDER = "images/players"

EXPORT_FOLDER = "images/exports"
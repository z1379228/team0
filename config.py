from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

ROOT = Path(__file__).parent

DATABASE = ROOT / "database" / "teambot.db"

PLAYER_FOLDER = ROOT / "images" / "players"

EXPORT_FOLDER = ROOT / "images" / "exports"

ASSET_FOLDER = ROOT / "assets"
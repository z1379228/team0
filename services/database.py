from pathlib import Path
import aiosqlite

import config


class Database:

    @staticmethod
    async def initialize():

        Path("database").mkdir(exist_ok=True)

        async with aiosqlite.connect(config.DATABASE) as db:

            await db.execute("PRAGMA foreign_keys = ON;")

            # 玩家資料
            await db.execute("""
            CREATE TABLE IF NOT EXISTS players(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                discord_id INTEGER UNIQUE,

                avatar TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 分隊歷史
            await db.execute("""
            CREATE TABLE IF NOT EXISTS team_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                team_hash TEXT UNIQUE,

                team_a TEXT NOT NULL,

                team_b TEXT NOT NULL,

                repeat_count INTEGER DEFAULT 1,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            await db.commit()

        print("✅ Database initialized")

    @staticmethod
    async def connect():

        db = await aiosqlite.connect(config.DATABASE)

        db.row_factory = aiosqlite.Row

        return db
from pathlib import Path
import aiosqlite

import config


class Database:

    @staticmethod
    async def initialize():

        Path("database").mkdir(exist_ok=True)

        async with aiosqlite.connect(config.DATABASE) as db:

            await db.execute("PRAGMA foreign_keys = ON;")

            # ==========================
            # 玩家資料
            # ==========================
            await db.execute("""
            CREATE TABLE IF NOT EXISTS players(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                discord_id INTEGER UNIQUE,

                avatar TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # ==========================
            # 房間
            # 一個頻道只能有一個房間
            # ==========================
            await db.execute("""
            CREATE TABLE IF NOT EXISTS rooms(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                guild_id INTEGER NOT NULL,

                channel_id INTEGER NOT NULL UNIQUE,

                owner_id INTEGER NOT NULL,

                status TEXT NOT NULL DEFAULT 'waiting',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # ==========================
            # 房間玩家
            # ==========================
            await db.execute("""
            CREATE TABLE IF NOT EXISTS room_players(

                room_id INTEGER NOT NULL,

                player_id INTEGER NOT NULL,

                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                PRIMARY KEY(room_id, player_id),

                FOREIGN KEY(room_id)
                    REFERENCES rooms(id)
                    ON DELETE CASCADE,

                FOREIGN KEY(player_id)
                    REFERENCES players(id)
                    ON DELETE CASCADE
            )
            """)

            # ==========================
            # 分隊歷史
            # ==========================
            await db.execute("""
            CREATE TABLE IF NOT EXISTS team_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                room_id INTEGER,

                team_hash TEXT NOT NULL,

                team_a TEXT NOT NULL,

                team_b TEXT NOT NULL,

                repeat_count INTEGER DEFAULT 1,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(room_id)
                    REFERENCES rooms(id)
                    ON DELETE SET NULL
            )
            """)

            await db.commit()

        print("✅ Database initialized")

    @staticmethod
    async def connect():

        db = await aiosqlite.connect(config.DATABASE)

        db.row_factory = aiosqlite.Row

        await db.execute("PRAGMA foreign_keys = ON;")

        return db
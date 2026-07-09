from models.player import Player
from services.database import Database


class PlayerService:

    @staticmethod
    async def create_discord_player(
        name: str,
        discord_id: int,
        avatar: str | None = None
    ) -> bool:

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT id
                FROM players
                WHERE discord_id = ?
                """,
                (discord_id,)
            )

            if await cursor.fetchone():
                return False

            await db.execute(
                """
                INSERT INTO players
                (
                    name,
                    discord_id,
                    avatar
                )
                VALUES
                (
                    ?, ?, ?
                )
                """,
                (
                    name,
                    discord_id,
                    avatar
                )
            )

            await db.commit()

            return True

    @staticmethod
    async def create_custom_player(
        name: str
    ) -> bool:

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT id
                FROM players
                WHERE discord_id IS NULL
                AND name = ?
                """,
                (name,)
            )

            if await cursor.fetchone():
                return False

            await db.execute(
                """
                INSERT INTO players
                (
                    name
                )
                VALUES
                (
                    ?
                )
                """,
                (name,)
            )

            await db.commit()

            return True

    @staticmethod
    async def get_player(
        player_id: int
    ) -> Player | None:

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM players
                WHERE id = ?
                """,
                (player_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return Player(
                id=row["id"],
                name=row["name"],
                discord_id=row["discord_id"],
                avatar=row["avatar"],
                created_at=row["created_at"]
            )

    @staticmethod
    async def get_all_players() -> list[Player]:

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM players
                ORDER BY name
                """
            )

            rows = await cursor.fetchall()

            players = []

            for row in rows:

                players.append(
                    Player(
                        id=row["id"],
                        name=row["name"],
                        discord_id=row["discord_id"],
                        avatar=row["avatar"],
                        created_at=row["created_at"]
                    )
                )

            return players

    @staticmethod
    async def delete_player(
        player_id: int
    ):

        async with await Database.connect() as db:

            await db.execute(
                """
                DELETE FROM players
                WHERE id = ?
                """,
                (player_id,)
            )

            await db.commit()
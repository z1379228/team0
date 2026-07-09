from models.room import Room
from models.player import Player
from services.database import Database


class RoomService:

    @staticmethod
    async def create_room(name, guild_id, channel_id, owner_id):

        async with await Database.connect() as db:

            cursor = await db.execute(
                "SELECT id FROM rooms WHERE channel_id=?",
                (channel_id,)
            )

            if await cursor.fetchone():
                return False

            await db.execute(
                """
                INSERT INTO rooms
                (name,guild_id,channel_id,owner_id,status)
                VALUES(?,?,?,?,?)
                """,
                (
                    name,
                    guild_id,
                    channel_id,
                    owner_id,
                    "waiting"
                )
            )

            await db.commit()

            return True

    @staticmethod
    async def get_room_by_channel(channel_id):

        async with await Database.connect() as db:

            cursor = await db.execute(
                "SELECT * FROM rooms WHERE channel_id=?",
                (channel_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return Room(
                id=row["id"],
                name=row["name"],
                guild_id=row["guild_id"],
                channel_id=row["channel_id"],
                owner_id=row["owner_id"],
                status=row["status"],
                created_at=row["created_at"]
            )

    @staticmethod
    async def delete_room(channel_id):

        async with await Database.connect() as db:

            await db.execute(
                "DELETE FROM rooms WHERE channel_id=?",
                (channel_id,)
            )

            await db.commit()

    @staticmethod
    async def add_player(room_id, player_id):

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM room_players
                WHERE room_id=?
                AND player_id=?
                """,
                (
                    room_id,
                    player_id
                )
            )

            if await cursor.fetchone():
                return False

            await db.execute(
                """
                INSERT INTO room_players
                (room_id,player_id)
                VALUES(?,?)
                """,
                (
                    room_id,
                    player_id
                )
            )

            await db.commit()

            return True

    @staticmethod
    async def remove_player(room_id, player_id):

        async with await Database.connect() as db:

            await db.execute(
                """
                DELETE FROM room_players
                WHERE room_id=?
                AND player_id=?
                """,
                (
                    room_id,
                    player_id
                )
            )

            await db.commit()

    @staticmethod
    async def get_players(room_id):

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT players.*
                FROM room_players
                JOIN players
                ON players.id=room_players.player_id
                WHERE room_players.room_id=?
                ORDER BY players.name
                """,
                (room_id,)
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
    async def get_player_count(room_id):

        players = await RoomService.get_players(room_id)

        return len(players)
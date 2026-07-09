from models.player import Player
from services.database import Database


class PlayerService:
    """玩家服務"""

    @staticmethod
    def _build_player(row) -> Player:
        """
        將資料庫查詢結果轉換成 Player 物件
        """

        return Player(
            id=row["id"],
            name=row["name"],
            discord_id=row["discord_id"],
            avatar=row["avatar"],
            created_at=row["created_at"],
        )

    @staticmethod
    async def create_discord_player(
        name: str,
        discord_id: int,
        avatar: str | None = None,
    ) -> bool:
        """
        建立 Discord 玩家
        """

        sql = """
        INSERT INTO players (
            name,
            discord_id,
            avatar
        )
        VALUES (?, ?, ?)
        """

        return await Database.execute(
            sql,
            (
                name,
                discord_id,
                avatar,
            ),
        )

    @staticmethod
    async def create_local_player(
        name: str,
    ) -> bool:
        """
        建立一般玩家
        """

        sql = """
        INSERT INTO players (
            name
        )
        VALUES (?)
        """

        return await Database.execute(
            sql,
            (
                name,
            ),
        )

    @staticmethod
    async def get_by_id(
        player_id: int,
    ) -> Player | None:
        """
        依 ID 取得玩家
        """

        sql = """
        SELECT
            id,
            name,
            discord_id,
            avatar,
            created_at
        FROM players
        WHERE id = ?
        """

        row = await Database.fetchone(
            sql,
            (
                player_id,
            ),
        )

        if row is None:
            return None

        return PlayerService._build_player(row)

    @staticmethod
    async def get_by_discord_id(
        discord_id: int,
    ) -> Player | None:
        """
        依 Discord ID 取得玩家
        """

        sql = """
        SELECT
            id,
            name,
            discord_id,
            avatar,
            created_at
        FROM players
        WHERE discord_id = ?
        """

        row = await Database.fetchone(
            sql,
            (
                discord_id,
            ),
        )

        if row is None:
            return None

        return PlayerService._build_player(row)

    @staticmethod
    async def get_by_name(
        name: str,
    ) -> Player | None:
        """
        依名稱取得玩家
        """

        sql = """
        SELECT
            id,
            name,
            discord_id,
            avatar,
            created_at
        FROM players
        WHERE name = ?
        """

        row = await Database.fetchone(
            sql,
            (
                name,
            ),
        )

        if row is None:
            return None

        return PlayerService._build_player(row)

    @staticmethod
    async def list_all() -> list[Player]:
        """
        取得所有玩家
        """

        sql = """
        SELECT
            id,
            name,
            discord_id,
            avatar,
            created_at
        FROM players
        ORDER BY id
        """

        rows = await Database.fetchall(sql)

        return [
            PlayerService._build_player(row)
            for row in rows
        ]

    @staticmethod
    async def update_name(
        player_id: int,
        name: str,
    ) -> bool:
        """
        更新玩家名稱
        """

        sql = """
        UPDATE players
        SET name = ?
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                name,
                player_id,
            ),
        )

    @staticmethod
    async def update_avatar(
        player_id: int,
        avatar: str | None,
    ) -> bool:
        """
        更新玩家頭像
        """

        sql = """
        UPDATE players
        SET avatar = ?
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                avatar,
                player_id,
            ),
        )

    @staticmethod
    async def bind_discord(
        player_id: int,
        discord_id: int,
        avatar: str | None = None,
    ) -> bool:
        """
        綁定 Discord 帳號
        """

        sql = """
        UPDATE players
        SET
            discord_id = ?,
            avatar = ?
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                discord_id,
                avatar,
                player_id,
            ),
        )

    @staticmethod
    async def unbind_discord(
        player_id: int,
    ) -> bool:
        """
        解除 Discord 綁定
        """

        sql = """
        UPDATE players
        SET
            discord_id = NULL,
            avatar = NULL
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                player_id,
            ),
        )

    @staticmethod
    async def exists_name(
        name: str,
    ) -> bool:
        """
        檢查玩家名稱是否存在
        """

        return await PlayerService.get_by_name(name) is not None

    @staticmethod
    async def exists_discord(
        discord_id: int,
    ) -> bool:
        """
        檢查 Discord 玩家是否存在
        """

        return await PlayerService.get_by_discord_id(discord_id) is not None

    @staticmethod
    async def delete(
        player_id: int,
    ) -> bool:
        """
        刪除玩家
        """

        sql = """
        DELETE FROM players
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                player_id,
            ),
        )
from models.team import Team
from services.database import Database


class TeamService:
    """隊伍服務"""

    @staticmethod
    def _build_team(row) -> Team:
        """
        將資料庫查詢結果轉換成 Team 物件
        """

        return Team(
            id=row["id"],
            name=row["name"],
            created_at=row["created_at"],
        )

    @staticmethod
    async def create(
        name: str,
    ) -> bool:
        """
        建立隊伍
        """

        sql = """
        INSERT INTO teams (
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
        team_id: int,
    ) -> Team | None:
        """
        依 ID 取得隊伍
        """

        sql = """
        SELECT
            id,
            name,
            created_at
        FROM teams
        WHERE id = ?
        """

        row = await Database.fetchone(
            sql,
            (
                team_id,
            ),
        )

        if row is None:
            return None

        return TeamService._build_team(row)

    @staticmethod
    async def get_by_name(
        name: str,
    ) -> Team | None:
        """
        依名稱取得隊伍
        """

        sql = """
        SELECT
            id,
            name,
            created_at
        FROM teams
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

        return TeamService._build_team(row)

    @staticmethod
    async def list_all() -> list[Team]:
        """
        取得所有隊伍
        """

        sql = """
        SELECT
            id,
            name,
            created_at
        FROM teams
        ORDER BY id
        """

        rows = await Database.fetchall(sql)

        return [
            TeamService._build_team(row)
            for row in rows
        ]
    @staticmethod
    async def update_name(
        team_id: int,
        name: str,
    ) -> bool:
        """
        更新隊伍名稱
        """

        sql = """
        UPDATE teams
        SET name = ?
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                name,
                team_id,
            ),
        )

    @staticmethod
    async def exists_name(
        name: str,
    ) -> bool:
        """
        檢查隊伍名稱是否存在
        """

        return await TeamService.get_by_name(name) is not None
    @staticmethod
    async def delete(
        team_id: int,
    ) -> bool:
        """
        刪除隊伍
        """

        sql = """
        DELETE FROM teams
        WHERE id = ?
        """

        return await Database.execute(
            sql,
            (
                team_id,
            ),
        )
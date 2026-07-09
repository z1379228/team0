from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from random import SystemRandom

from models.player import Player
from models.team import Team


class TeamService:
    """隊伍生成服務。"""

    _MIN_PLAYERS = 2

    @classmethod
    def generate(cls, players: list[Player]) -> tuple[Team, Team, str]:
        """
        產生兩隊隊伍並回傳隊伍與雜湊值。

        Args:
            players:
                玩家清單。

        Returns:
            tuple[Team, Team, str]:
                Team A、Team B 與隊伍雜湊值。
        """

        cloned_players = cls._clone_players(players)
        cls._validate_players(cloned_players)

        shuffled_players = cls._shuffle(cloned_players)
        team_a_players, team_b_players = cls._split(shuffled_players)

        team_a = cls._normalize(
            Team(
                id=0,
                name="Team A",
                players=team_a_players,
            )
        )

        team_b = cls._normalize(
            Team(
                id=0,
                name="Team B",
                players=team_b_players,
            )
        )

        team_hash = cls._calculate_hash(team_a, team_b)

        return team_a, team_b, team_hash

    @staticmethod
    def _clone_players(players: list[Player]) -> list[Player]:
        """
        建立玩家清單副本，避免修改外部資料。

        Args:
            players:
                原始玩家清單。

        Returns:
            list[Player]:
                深層複製後的玩家清單。
        """

        return deepcopy(players)

    @classmethod
    def _validate_players(cls, players: list[Player]) -> None:
        """
        驗證玩家資料是否合法。

        Args:
            players:
                玩家清單。

        Raises:
            ValueError:
                玩家數量不足、存在重複玩家或玩家名稱無效。
        """

        if len(players) < cls._MIN_PLAYERS:
            raise ValueError("At least two players are required.")

        ids: set[int] = set()

        for player in players:
            if player.id in ids:
                raise ValueError("Duplicate player detected.")

            ids.add(player.id)

            if not player.name.strip():
                raise ValueError("Player name cannot be empty.")
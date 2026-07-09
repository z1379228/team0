from dataclasses import dataclass, field

from models.player import Player


@dataclass(slots=True)
class Team:
    """
    Represents a team of players.
    """

    players: list[Player] = field(default_factory=list)

    @property
    def size(self) -> int:
        """
        Returns the number of players in the team.
        """
        return len(self.players)

    @property
    def is_empty(self) -> bool:
        """
        Returns whether the team contains no players.
        """
        return not self.players

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.
        """
        self.players.append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.
        """
        self.players.remove(player)

    def clear(self) -> None:
        """
        Removes all players from the team.
        """
        self.players.clear()
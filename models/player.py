from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Player:

    id: int

    name: str

    discord_id: int | None

    avatar: str | None

    is_guest: bool

    created_at: datetime | None = None

    @property
    def is_discord(self) -> bool:
        return self.discord_id is not None

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def avatar_path(self) -> str | None:
        return self.avatar
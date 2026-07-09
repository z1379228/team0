from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Room:

    id: int

    name: str

    guild_id: int

    channel_id: int

    owner_id: int

    status: str

    created_at: datetime | None = None

    @property
    def is_waiting(self) -> bool:
        return self.status == "waiting"

    @property
    def is_started(self) -> bool:
        return self.status == "started"

    @property
    def is_closed(self) -> bool:
        return self.status == "closed"
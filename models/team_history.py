from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class TeamHistory:

    id: int

    room_id: int | None

    team_hash: str

    team_a: str

    team_b: str

    repeat_count: int

    created_at: datetime | None = None
from pydantic import BaseModel


class StandingRow(BaseModel):
    position: int
    team_id: int
    team_name: str
    points: int
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_diff: int
    status: str | None = None

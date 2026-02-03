from pydantic import BaseModel
from typing import Optional


class MatchResult(BaseModel):
    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]
    played: bool

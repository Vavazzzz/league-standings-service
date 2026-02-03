from pydantic import BaseModel


class Scorer(BaseModel):
    """Modello per un marcatore"""
    name: str
    player_id: int | None = None


class MatchResult(BaseModel):
    match_day: int
    date: str | None
    time: str | None
    home_team: str
    home_team_id: int
    away_team: str
    away_team_id: int
    home_score: int | None
    away_score: int | None
    home_scorers: list[Scorer] = []
    away_scorers: list[Scorer] = []

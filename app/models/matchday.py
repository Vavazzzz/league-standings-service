from pydantic import BaseModel
from typing import Optional
from app.models.matchresult import MatchResult as Match


class MatchDay(BaseModel):
    """Modello per una giornata di partite"""
    match_day: int
    matches: list[Match]

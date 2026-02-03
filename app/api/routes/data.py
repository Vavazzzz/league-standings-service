from fastapi import APIRouter, Query
from app.models.standings import StandingRow
from app.models.matchresult import MatchResult
from app.models.matchday import MatchDay
from app.scrapers.ranking_scraper import fetch_standings
from app.scrapers.result_scraper import fetch_results
from app.scrapers.matchday_scraper import fetch_next_matches

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/standings", response_model=list[StandingRow])
def get_standings(match_day: int | None = Query(None)):
    """Ottiene la classifica per una giornata specifica o totale
    
    Args:
        match_day: Numero della giornata (opzionale per classifica totale)
    
    Returns:
        Lista di StandingRow ordinata per posizione
    """
    return fetch_standings(match_day)


@router.get("/results", response_model=list[MatchResult])
def get_results(match_day: int = Query(...)):
    """Ottiene i risultati per una giornata specifica
    
    Args:
        match_day: Numero della giornata
    
    Returns:
        Lista di MatchResult
    """
    return fetch_results(match_day)


@router.get("/matchday", response_model=MatchDay)
def get_matchday(match_day: int = Query(...)):
    """Ottiene tutti i dati di una giornata (partite)
    
    Args:
        match_day: Numero della giornata
    
    Returns:
        MatchDay con tutti i dati della giornata
    """
    return fetch_next_matches(match_day)

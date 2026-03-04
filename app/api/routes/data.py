from fastapi import APIRouter, Query
from app.models.standings import StandingRow
from app.models.matchresult import MatchResult
from app.models.matchday import MatchDay
from app.scrapers.standings_scraper import fetch_standings
from app.scrapers.result_scraper import fetch_results, fetch_match_by_team
from app.scrapers.matchday_scraper import fetch_next_matches, fetch_next_match_by_team

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/standings", response_model=list[StandingRow])
def get_standings(match_day: int | None = Query(None), team_id: str = Query("1")):
    """Ottiene la classifica per una giornata specifica o totale
    
    Args:
        match_day: Numero della giornata (opzionale per classifica totale)
        team_id: ID del team (default: "1")
    
    Returns:
        Lista di StandingRow ordinata per posizione
    """
    return fetch_standings(match_day, team_id)


@router.get("/results", response_model=list[MatchResult])
def get_results(match_day: int = Query(...), team_id: str = Query("1")):
    """Ottiene i risultati per una giornata specifica
    
    Args:
        match_day: Numero della giornata
        team_id: ID del team (default: "1")
    
    Returns:
        Lista di MatchResult
    """
    return fetch_results(match_day, team_id)


@router.get("/results/team", response_model=MatchResult | None)
def get_team_match(match_day: int = Query(...), team_name: str = Query(...), team_id: str = Query("1")):
    """Ottiene il risultato della partita di una squadra specifica
    
    Args:
        match_day: Numero della giornata
        team_name: Nome della squadra
        team_id: ID del team (default: "1")
    
    Returns:
        MatchResult con i dati della partita della squadra
    """
    return fetch_match_by_team(match_day, team_name, team_id)


@router.get("/matchday", response_model=MatchDay)
def get_matchday(match_day: int = Query(...), team_id: str = Query("1")):
    """Ottiene tutti i dati di una giornata (partite)
    
    Args:
        match_day: Numero della giornata
        team_id: ID del team (default: "1")
    
    Returns:
        MatchDay con tutti i dati della giornata
    """
    return fetch_next_matches(match_day, team_id)


@router.get("/matchday/team", response_model=MatchDay)
def get_matchday_by_team(match_day: int = Query(...), team_name: str = Query(...), team_id: str = Query("1")):
    """Ottiene tutti i dati di una giornata (partite) per una squadra specifica
    
    Args:
        match_day: Numero della giornata
        team_name: Nome della squadra
        team_id: ID del team (default: "1")
    
    Returns:
        MatchDay con tutti i dati della giornata
    """
    return fetch_next_match_by_team(match_day, team_name, team_id)
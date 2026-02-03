from app.models.matchday import MatchDay
from app.scrapers.result_scraper import fetch_results


def fetch_next_matches(match_day: int) -> MatchDay:
    """Fetcha le prossime partite per una giornata specifica
    
    Args:
        match_day: Numero della giornata
    
    Returns:
        MatchDay con i dati delle partite
    """
    results = fetch_results(match_day)
    
    return MatchDay(
        match_day=match_day,
        matches=results
    )

def fetch_next_match_by_team(match_day: int, team_name: str) -> MatchDay:
    """Fetcha e parsa la prossima giornata, restituendo solo la partita di una squadra specifica
    
    Args:
        match_day: Numero della giornata
        team_name: Nome della squadra (cerca home_team o away_team)
    
    Returns:
        MatchDay della partita della squadra, o None se non trovata
    """
    matches = fetch_next_matches(match_day)
    
    for match in matches.matches:
        if match.home_team.lower() == team_name.lower() or match.away_team.lower() == team_name.lower():
            return MatchDay(
                match_day=match_day,
                matches=[match]
            )
    
    return None
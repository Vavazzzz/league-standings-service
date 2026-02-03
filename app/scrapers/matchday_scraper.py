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

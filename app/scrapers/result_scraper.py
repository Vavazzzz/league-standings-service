from bs4 import BeautifulSoup
from app.models.matchresult import MatchResult
from app.scrapers.tuttocampo_client import TuttoCampoClient
import re


def parse_results(html: str, match_day: int | None = None) -> list[MatchResult]:
    """Parsa l'HTML dei risultati e restituisce una lista di MatchResult
    
    Args:
        html: HTML da parsare
        match_day: Numero della giornata (se non presente nell'HTML, usa questo)
    
    Returns:
        Lista di MatchResult
    """
    soup = BeautifulSoup(html, "lxml")

    # Estrai match_day dall'HTML se disponibile
    match_day_element = soup.select_one("#match_day")
    if match_day_element:
        match_day_text = match_day_element.text
        match_day = int(re.search(r"\d+", match_day_text).group())

    matches = []
    current_date = None

    for row in soup.select("table.table-results tbody tr"):
        if "date" in row.get("class", []):
            current_date = row.text.strip()
            continue

        if "match" not in row.get("class", []):
            continue

        home = row.select_one("td.home")
        away = row.select_one("td.away")
        time_cell = row.select_one(".match-time")

        score_span = row.select_one(".goal")

        home_score = None
        away_score = None

        if score_span and "-" in score_span.text:
            h, a = score_span.text.split("-")
            home_score = int(h.strip())
            away_score = int(a.strip())

        matches.append(
            MatchResult(
                match_day=match_day,
                date=current_date,
                time=time_cell.text.strip() if time_cell else None,
                home_team=home.select_one(".team-name").text.strip(),
                home_team_id=int(home["data-team-id"]),
                away_team=away.select_one(".team-name").text.strip(),
                away_team_id=int(away["data-team-id"]),
                home_score=home_score,
                away_score=away_score
            )
        )

    return matches


def fetch_results(match_day: int) -> list[MatchResult]:
    """Fetcha e parsa i risultati da TuttoCampo per una giornata specifica
    
    Args:
        match_day: Numero della giornata
    
    Returns:
        Lista di MatchResult
    """
    client = TuttoCampoClient()
    html = client.fetch_results(match_day)
    return parse_results(html, match_day)

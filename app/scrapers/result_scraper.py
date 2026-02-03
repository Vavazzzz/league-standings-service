from bs4 import BeautifulSoup
from app.models.matchresult import MatchResult, Scorer
from app.scrapers.tuttocampo_client import TuttoCampoClient
import re


def extract_scorers(team_section) -> list[Scorer]:
    """Estrae la lista dei marcatori da una sezione squadra
    
    Args:
        team_section: L'elemento td con classe team (home o away)
    
    Returns:
        Lista di Scorer
    """
    scorers = []
    scorers_list = team_section.select("ul.scorers li a")
    
    for scorer_link in scorers_list:
        player_name = scorer_link.text.strip()
        
        # Estrai l'ID del giocatore dall'href se disponibile
        href = scorer_link.get("href", "")
        player_id = None
        match = re.search(r"/(\d+)/", href)
        if match:
            try:
                player_id = int(match.group(1))
            except (ValueError, AttributeError):
                pass
        
        scorers.append(Scorer(name=player_name, player_id=player_id))
    
    return scorers


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

    results = []
    current_date = None

    # Seleziona tutte le righe della tabella risultati
    for row in soup.select("table.table-results tbody tr"):
        # Se è una riga di data, aggiorna la data corrente
        if "date" in row.get("class", []):
            current_date = row.text.strip()
            continue

        # Se non è una riga di partita, salta
        if "match" not in row.get("class", []):
            continue

        # Estrai le sezioni home e away
        home_section = row.select_one("td.team.home")
        away_section = row.select_one("td.team.away")
        
        if not home_section or not away_section:
            continue

        # Estrai l'orario della partita
        time_cell = row.select_one("td.match-time span.hour")
        time_str = time_cell.text.strip() if time_cell else None

        # Estrai i dati della squadra di casa
        home_team_name = home_section.select_one("a.team-name").text.strip()
        home_team_id = int(home_section.get("data-team-id"))
        
        # Estrai lo score della squadra di casa
        home_goal_span = home_section.select_one("a span.goal")
        home_score = None
        if home_goal_span and home_goal_span.text.strip():
            try:
                home_score = int(home_goal_span.text.strip())
            except ValueError:
                pass

        # Estrai i dati della squadra in trasferta
        away_team_name = away_section.select_one("a.team-name").text.strip()
        away_team_id = int(away_section.get("data-team-id"))
        
        # Estrai lo score della squadra in trasferta
        away_goal_span = away_section.select_one("a span.goal")
        away_score = None
        if away_goal_span and away_goal_span.text.strip():
            try:
                away_score = int(away_goal_span.text.strip())
            except ValueError:
                pass

        # Estrai i marcatori
        home_scorers = extract_scorers(home_section)
        away_scorers = extract_scorers(away_section)

        results.append(
            MatchResult(
                match_day=match_day,
                date=current_date,
                time=time_str,
                home_team=home_team_name,
                home_team_id=home_team_id,
                away_team=away_team_name,
                away_team_id=away_team_id,
                home_score=home_score,
                away_score=away_score,
                home_scorers=home_scorers,
                away_scorers=away_scorers
            )
        )

    return results


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


def fetch_match_by_team(match_day: int, team_name: str) -> MatchResult | None:
    """Fetcha e parsa i risultati, restituendo solo la partita di una squadra specifica
    
    Args:
        match_day: Numero della giornata
        team_name: Nome della squadra (cerca home_team o away_team)
    
    Returns:
        MatchResult della partita della squadra, o None se non trovata
    """
    results = fetch_results(match_day)
    
    for match in results:
        if match.home_team.lower() == team_name.lower() or match.away_team.lower() == team_name.lower():
            return match
    
    return None


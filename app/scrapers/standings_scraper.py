from bs4 import BeautifulSoup
from app.models.standings import StandingRow
from app.scrapers.tuttocampo_client import TuttoCampoClient


def parse_ranking(html: str) -> list[StandingRow]:
    """Parsa l'HTML della classifica e restituisce una lista di StandingRow"""
    soup = BeautifulSoup(html, "lxml")

    rows = soup.select("table.table_ranking tbody tr")

    standings = []
    position = 1

    for row in rows:
        team_cell = row.select_one("td.team a")
        if not team_cell:
            continue

        status = None
        classes = row.get("class", [])
        if classes:
            status = classes[0] if classes[0] not in ["", None] else None

        cells = row.find_all("td")

        standings.append(
            StandingRow(
                position=position,
                team_id=int(row["data-team-id"]),
                team_name=team_cell.text.strip(),
                points=int(row.select_one(".points").text),
                played=int(cells[4].text),
                wins=int(cells[5].text),
                draws=int(cells[6].text),
                losses=int(cells[7].text),
                goals_for=int(cells[8].text),
                goals_against=int(cells[9].text),
                goal_diff=int(cells[10].text),
                status=status
            )
        )

        position += 1

    return standings


def fetch_standings(match_day: int | None = None) -> list[StandingRow]:
    """Fetcha e parsa la classifica da TuttoCampo
    
    Args:
        match_day: Numero della giornata (None per classifica totale)
    
    Returns:
        Lista di StandingRow
    """
    client = TuttoCampoClient()
    html = client.fetch_standings(match_day)
    return parse_ranking(html)

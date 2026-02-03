from bs4 import BeautifulSoup
from models.matchresult import MatchResult
import re


def parse_results(html: str) -> list[MatchResult]:

    soup = BeautifulSoup(html, "lxml")

    match_day_text = soup.select_one("#match_day").text
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

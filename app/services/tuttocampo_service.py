from app.scrapers.tuttocampo_client import TuttoCampoClient
from app.scrapers.standings_scraper import parse_ranking
from app.scrapers.result_scraper import parse_results


class TuttoCampoService:

    def __init__(self, team_id: str = "1"):
        self.team_id = team_id
        self.client = TuttoCampoClient(team_id=team_id)

    def get_standings(self, match_day: int | None = None):
        """Get standings for a specific matchday or total"""
        html = self.client.fetch_standings(match_day)
        return parse_ranking(html)

    def get_results(self, match_day: int):
        """Get results for a specific matchday"""
        html = self.client.fetch_results(match_day)
        return parse_results(html, match_day)